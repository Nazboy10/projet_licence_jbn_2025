# app_bulletin/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from app_eleve.models import Eleve
from app_note.models import Note
from .models import Bulletin
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ 1. Vue principale : affiche le template HTML
def bulletin(request):
    return render(request, "app_bulletin/bulletin.html")

# ✅ 2. Vue API : génère et sauvegarde le bulletin
@require_http_methods(["GET"])
def api_bulletin_eleve(request):
    code = request.GET.get('code')
    periode = request.GET.get('periode', '1er_trimestre')

    if not code:
        return JsonResponse({'erreur': 'Code élève requis'}, status=400)

    try:
        eleve = Eleve.objects.get(code_eleve=code, actif=True)
        notes_qs = Note.objects.filter(eleve=eleve, periode=periode).select_related('matiere')

        if not notes_qs.exists():
            return JsonResponse({'erreur': f'Aucune note pour la période {periode}'}, status=404)

        notes = []
        total_coef = 0
        total_pondere = 0
        for note in notes_qs:
            coef = 1
            val = float(note.valeur)
            pond = val * coef
            total_coef += coef
            total_pondere += pond
            notes.append({
                'matiere': note.matiere.nom,
                'coef': coef,
                'note': val,
                'pondere': pond
            })

        moyenne = total_pondere / total_coef if total_coef else 0
        mention = (
            "Excellent" if moyenne >= 16 else
            "Très Bien" if moyenne >= 14 else
            "Bien" if moyenne >= 12 else
            "Assez Bien" if moyenne >= 10 else
            "Insuffisant"
        )

        # ✅ Sauvegarde du bulletin
        user_id = request.session.get('id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                Bulletin.objects.get_or_create(
                    eleve=eleve,
                    periode=periode,
                    defaults={
                        'moyenne': round(moyenne, 2),
                        'mention': mention,
                        'genere_par': user
                    }
                )
            except User.DoesNotExist:
                pass  # ou log

        return JsonResponse({
            'eleve': {
                'code': eleve.code_eleve,
                'nom': eleve.nom,
                'prenom': eleve.prenom,
                'classe': eleve.classe,
            },
            'notes': notes,
            'periode': periode,
            'total_pondere': round(total_pondere, 2),
            'moyenne': round(moyenne, 2),
            'mention': mention
        })

    except Eleve.DoesNotExist:
        return JsonResponse({'erreur': 'Élève non trouvé'}, status=404)









# app_bulletin/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from app_eleve.models import Eleve
from app_note.models import Note
from .models import Bulletin
from SGCBA.models import Utilisateur  # ← IMPORT DIRECT

User = Utilisateur  # ← PAS get_user_model()

# ... (ta vue bulletin et api_bulletin_eleve inchangées)

@csrf_protect
@require_http_methods(["POST"])
def api_enregistrer_bulletin(request):
    import json
    try:
        data = json.loads(request.body)
        code_eleve = data.get('code')
        periode = data.get('periode', '1er_trimestre')

        if not code_eleve:
            return JsonResponse({'erreur': 'Code élève requis'}, status=400)

        eleve = Eleve.objects.get(code_eleve=code_eleve, actif=True)
        notes_qs = Note.objects.filter(eleve=eleve, periode=periode)

        if not notes_qs.exists():
            return JsonResponse({'erreur': 'Aucune note pour cet élève'}, status=404)

        total_coef = 0
        total_pondere = 0
        for note in notes_qs:
            coef = 1
            val = float(note.valeur)
            total_coef += coef
            total_pondere += val * coef

        moyenne = total_pondere / total_coef if total_coef else 0
        mention = (
            "Excellent" if moyenne >= 16 else
            "Très Bien" if moyenne >= 14 else
            "Bien" if moyenne >= 12 else
            "Assez Bien" if moyenne >= 10 else
            "Insuffisant"
        )

        user_id = request.session.get('id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)  # ← Utilisateur, pas auth.User
                bulletin, created = Bulletin.objects.get_or_create(
                    eleve=eleve,
                    periode=periode,
                    defaults={'moyenne': round(moyenne, 2), 'mention': mention, 'genere_par': user}
                )
                return JsonResponse({'success': True, 'message': 'Bulletin enregistré.', 'created': created})
            except User.DoesNotExist:
                return JsonResponse({'erreur': 'Utilisateur invalide'}, status=400)
        else:
            return JsonResponse({'erreur': 'Non authentifié'}, status=401)

    except Eleve.DoesNotExist:
        return JsonResponse({'erreur': 'Élève non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'erreur': 'Erreur serveur'}, status=500)










@require_http_methods(["GET"])
def api_liste_eleves_pour_bulletin(request):
    # ✅ Sèl chanjman: "note" → "notes" (avèk "s")
    eleves_avec_notes = Eleve.objects.filter(
        notes__isnull=False,  # ← ICI: "notes", pa "note"
        actif=True
    ).distinct().values(
        'code_eleve',
        'nom',
        'prenom',
        'classe'
    )

    liste = [
        {
            'code': e['code_eleve'],
            'nom': e['nom'],
            'prenom': e['prenom'],
            'classe': e['classe'] or 'Non spécifiée'
        }
        for e in eleves_avec_notes
    ]

    return JsonResponse(liste, safe=False)