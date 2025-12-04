# app_note/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import Note, Matiere
from app_eleve.models import Eleve  # ajuste selon ton app
from SGCBA.utils import verify_active_session  # Assure-toi que ce chemin est correct


def note(request):
    # Optionnel : vérifier le rôle ici ou via middleware
    error = verify_active_session(request)
    if error:
        return error
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
from app_parametre.models import Parametre
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

        param = Parametre.load()
        trimestre_actif = param.trimestre  # ex: 1, 2, 3
        annee_actuelle = param.annee_academique  # ex: "2025-2026"

        PERIODE_MAP = {
            1: '1er_trimestre',
            2: '2eme_trimestre',
            3: '3eme_trimestre',
        }
        periode_actif = PERIODE_MAP.get(trimestre_actif, '1er_trimestre')  # defo: 1er_trimestre



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

            if not (0 <= float(valeur) <= 100):
                return JsonResponse({'erreur': f'Note invalide : {valeur}'}, status=400)

            Note.objects.update_or_create(
                eleve=eleve,
                matiere_id=matiere_id,
                periode=periode_actif,  
                annee_academique=annee_actuelle,
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
from SGCBA.utils import verify_active_session

def gestion_matieres(request):
    error = verify_active_session(request)
    if error:
        return error

    role = request.session.get('role')
    
    # Seul le directeur peut ajouter/supprimer
    if role != 'directeur':
        messages.error(request, "Accès réservé au directeur.")
        return redirect('tableau_de_bord')

    if request.method == "POST":
        # Ajout
        if 'nom' in request.POST:
            nom = request.POST.get('nom', '').strip()
            if nom and not Matiere.objects.filter(nom__iexact=nom).exists():
                Matiere.objects.create(nom=nom)
                messages.success(request, f"La matière '{nom}' a été ajoutée.")
            else:
                messages.error(request, "Nom invalide ou matière déjà existante.")
        
        # Suppression
        elif 'matiere_id' in request.POST:
            matiere_id = request.POST.get('matiere_id')
            try:
                matiere = Matiere.objects.get(id=matiere_id)
                matiere.delete()
                messages.success(request, f"La matière '{matiere.nom}' a été supprimée.")
            except Matiere.DoesNotExist:
                messages.error(request, "Matière non trouvée.")

        return redirect('gestion_matieres')

    matieres = Matiere.objects.all().order_by('nom')
    return render(request, 'app_note/gestion_matieres.html', {
        'matieres': matieres,
        'role': role
    })


# lister notes avec regroupement par élève et période

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Note

@require_http_methods(["GET"])
def lister_notes(request):
    notes = Note.objects.select_related('eleve', 'matiere').all()

    # Regroupement par (élève, période)
    groupe = {}
    for note in notes:
        key = (note.eleve.code_eleve, note.periode)
        if key not in groupe:
            groupe[key] = {
                'code_eleve': note.eleve.code_eleve,
                'nom': note.eleve.nom,
                'prenom': note.eleve.prenom,
                'classe': str(note.eleve.classe) if note.eleve.classe else 'Non spécifiée',
                'periode': note.periode,  # ✅ On inclut la période ici
                'matieres_notes': []
            }
        groupe[key]['matieres_notes'].append({
            'matiere': note.matiere.nom,
            'valeur': float(note.valeur)
        })

    return JsonResponse(list(groupe.values()), safe=False)



from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Note
from app_eleve.models import Eleve

@require_http_methods(["DELETE"])
def supprimer_notes_eleve(request, code_eleve):
    try:
        # Vérifier l'authentification via session
        if 'id' not in request.session:
            return JsonResponse({'erreur': 'Non authentifié'}, status=401)

        # Charger la période et année académique actives
        from app_parametre.models import Parametre
        param = Parametre.load()
        trimestre_actif = param.trimestre
        annee_actuelle = param.annee_academique

        PERIODE_MAP = {
            1: '1er_trimestre',
            2: '2eme_trimestre',
            3: '3eme_trimestre',
        }
        periode_actif = PERIODE_MAP.get(trimestre_actif, '1er_trimestre')

        # Trouver l'élève
        eleve = get_object_or_404(Eleve, code_eleve=code_eleve, actif=True)

        # Supprimer toutes les notes de cet élève pour la période + année actives
        deleted_count, _ = Note.objects.filter(
            eleve=eleve,
            periode=periode_actif,
            annee_academique=annee_actuelle
        ).delete()

        if deleted_count == 0:
            return JsonResponse({'message': 'Aucune note à supprimer pour cette période.'}, status=200)

        return JsonResponse({'success': True, 'message': f'{deleted_count} note(s) supprimée(s).'})

    except Exception as e:
        print("Erreur suppression :", str(e))
        return JsonResponse({'erreur': 'Erreur serveur.'}, status=500)
    











from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Note, Matiere
from app_eleve.models import Eleve
from app_parametre.models import Parametre
from SGCBA.models import Utilisateur
import json

@require_http_methods(["PUT"])
def modifier_notes_eleve(request):
    try:
        if 'id' not in request.session:
            return JsonResponse({'erreur': 'Non authentifié'}, status=401)

        user_id = request.session['id']
        saisi_par = get_object_or_404(Utilisateur, id=user_id)

        param = Parametre.load()
        trimestre_actif = param.trimestre
        annee_actuelle = param.annee_academique

        PERIODE_MAP = {
            1: '1er_trimestre',
            2: '2eme_trimestre',
            3: '3eme_trimestre',
        }
        periode_actif = PERIODE_MAP.get(trimestre_actif, '1er_trimestre')

        data = json.loads(request.body)
        code_eleve = data.get('code_eleve')
        notes_data = data.get('notes', [])

        if not code_eleve or not notes_data:
            return JsonResponse({'erreur': 'Données manquantes'}, status=400)

        eleve = get_object_or_404(Eleve, code_eleve=code_eleve, actif=True)

        # Supprimer les anciennes notes pour cet élève, période et année
        Note.objects.filter(
            eleve=eleve,
            periode=periode_actif,
            annee_academique=annee_actuelle
        ).delete()

        # Ré-insérer les nouvelles notes
        for item in notes_data:
            matiere_id = item.get('matiere_id')
            valeur = item.get('valeur')

            if not matiere_id or valeur is None:
                return JsonResponse({'erreur': 'Matière ou note manquante'}, status=400)

            if not (0 <= float(valeur) <= 100):
                return JsonResponse({'erreur': f'Note invalide : {valeur}'}, status=400)

            Note.objects.create(
                eleve=eleve,
                matiere_id=matiere_id,
                periode=periode_actif,
                annee_academique=annee_actuelle,
                valeur=valeur,
                saisi_par=saisi_par
            )

        return JsonResponse({'success': True, 'message': 'Notes modifiées avec succès.'})

    except Exception as e:
        print("Erreur modification :", str(e))
        return JsonResponse({'erreur': 'Erreur serveur.'}, status=500)