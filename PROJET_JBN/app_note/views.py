# app_note/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import Note, Matiere
from app_eleve.models import Eleve  # ajuste selon ton app


def note(request):
    # Optionnel : vérifier le rôle ici ou via middleware
    return render(request, "app_note/note.html")

@require_http_methods(["POST"])

def verifier_code_eleve(request):
    code = request.POST.get('code')
    try:
       # app_note/views.py
        eleve = Eleve.objects.get(code_eleve=code, actif=True)  # seulement les élèves validés
        return JsonResponse({
            'existe': True,
            'nom': eleve.nom,
            'prenom': eleve.prenom,
            'classe': str(eleve.classe),
        })
    except Eleve.DoesNotExist:
        return JsonResponse({'existe': False})

@require_http_methods(["GET"])

def lister_matieres(request):
    matieres = Matiere.objects.all().values('id', 'nom')
    return JsonResponse(list(matieres), safe=False)

# app_note/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Note, Matiere
from app_eleve.models import Eleve
from SGCBA.models import Utilisateur  # ← ajuste si ton modèle s'appelle autrement
# app_note/views.py

import traceback  # ← ajoute ceci en haut du fichier

@require_http_methods(["POST"])
def enregistrer_notes(request):
    import json
    try:
        if 'id' not in request.session:
            return JsonResponse({'erreur': 'Non authentifié'}, status=401)

        user_id = request.session['id']
        saisi_par = get_object_or_404(Utilisateur, id=user_id)

        data = json.loads(request.body)
        code_eleve = data.get('code_eleve')
        notes_data = data.get('notes', [])

        if not code_eleve or not notes_data:
            return JsonResponse({'erreur': 'Données manquantes'}, status=400)

        eleve = get_object_or_404(Eleve, code_eleve=code_eleve, actif=True)

        for item in notes_data:
            matiere_id = item.get('matiere_id')
            valeur = item.get('valeur')

            if not matiere_id or valeur is None:
                return JsonResponse({'erreur': 'Matière ou note manquante'}, status=400)

            if not (0 <= float(valeur) <= 20):
                return JsonResponse({'erreur': f'Note invalide : {valeur}'}, status=400)

            Note.objects.update_or_create(
                eleve=eleve,
                matiere_id=matiere_id,
                defaults={'valeur': valeur, 'saisi_par': saisi_par}
            )

        return JsonResponse({'success': True, 'message': 'Notes enregistrées avec succès.'})

    except Exception as e:
        # 🚨 TEMPORAIRE : affiche l'erreur réelle dans la console ET dans la réponse
        print("🚨 ERREUR DANS enregistrer_notes :", str(e))
        print(traceback.format_exc())  # ← affiche la stack complète
        return JsonResponse({'erreur': str(e)}, status=400)  # ← juste pour le debug





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Matiere

# app_note/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Matiere

def gestion_matieres(request):
    # ✅ Vérifie via la session, PAS request.user
    if 'role' not in request.session:
        return redirect('connexion')  # ou ta page de login

    if request.session['role'] != 'directeur':
        messages.error(request, "Accès réservé au directeur.")
        return redirect('tableau_de_bord')

    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom and not Matiere.objects.filter(nom__iexact=nom).exists():
            Matiere.objects.create(nom=nom)
            messages.success(request, f"Matière '{nom}' ajoutée.")
        else:
            messages.warning(request, "Matière vide ou déjà existante.")
        return redirect('gestion_matieres')

    matieres = Matiere.objects.all().order_by('nom')
    return render(request, 'app_note/gestion_matieres.html', {'matieres': matieres})







# app_note/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Note

@require_http_methods(["GET"])
def lister_notes(request):
    # Récupère toutes les notes
    notes = Note.objects.select_related('eleve', 'matiere').all()
    
    # Regroupe par élève
    eleves_notes = {}
    for note in notes:
        code = note.eleve.code_eleve
        if code not in eleves_notes:
            eleves_notes[code] = {
                'code_eleve': code,
                'nom': note.eleve.nom,
                'prenom': note.eleve.prenom,
                'classe': note.eleve.classe,
                'matieres_notes': []  # liste des {matiere: nom, valeur: float}
            }
        eleves_notes[code]['matieres_notes'].append({
            'matiere': note.matiere.nom,
            'valeur': float(note.valeur)
        })

    return JsonResponse(list(eleves_notes.values()), safe=False)