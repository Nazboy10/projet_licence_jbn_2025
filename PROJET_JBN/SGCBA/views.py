from django.shortcuts import render, redirect
from SGCBA.models import Utilisateur  # Asire modèl ou importé
from app_inscription.models import Inscription
from app_eleve.models import Eleve
from SGCBA.utils import verify_active_session 
from django.db.models import Avg

from app_note.models import Note
# view pou splashScreen lan
def splash(request):
    return render(request, 'splash.html')

# view pou dashboard la
def tableau_de_bord(request):
    error = verify_active_session(request)  # ✅ Vérification
    if error:
        return error  # Si itilizatè pa konekte
    
     # Kalkile kantite enskripsyon total
    total_inscriptions = Inscription.objects.count()
    total_eleve = Eleve.objects.count()

    #   # 1️⃣ Kalkile mwayèn chak elèv
    # eleves_moyennes = Note.objects.values('eleve').annotate(moyenne=Avg('valeur'))

    # # 2️⃣ Konte elèv ki gen mwayèn >= 10
    # total_reussite = sum(1 for e in eleves_moyennes if e['moyenne'] >= 10)

    # # 3️⃣ Taux de réussite (%)
    # taux_reussite = 0
    # if total_eleve > 0:
    #     taux_reussite = round((total_reussite / total_eleve) * 100, 2)


    context = {
        'username': request.session['username'],
        'role': request.session['role'],
        'total_inscriptions': total_inscriptions,
         'total_eleve':  total_eleve,
        #   'taux_reussite': taux_reussite,
    }
    return render(request, 'tableau_de_bord.html', context)

# views pou meni yo
def inscription(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'inscription.html')

def eleve(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'dossier_eleves.html')

def presence(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'presence.html')

def note(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'notes.html')

def bulletin(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'bulletin.html')

def utilisateurs(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'utilisateurs.html')

def parametre(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'parametres.html')


# views.py

from app_parametre.models import Parametre

def connexion(request):
    param = Parametre.load()
    print("DEBUG: param.pw_reset =", param.pw_reset)
    print("DEBUG: type =", type(param.pw_reset))
    return render(request, 'connexion.html', {'pw_reset_enabled': param.pw_reset})

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from SGCBA.models import Utilisateur

@login_required
def changer_photo(request):
    user_id = request.session.get('id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Utilisateur non connecté'}, status=401)

    user = Utilisateur.objects.get(id=user_id)

    if request.method == 'POST' and request.FILES.get('photo'):
        user.photo = request.FILES['photo']
        user.save()
        return JsonResponse({'success': True, 'photo_url': user.photo.url})

    return JsonResponse({'success': False, 'message': 'Aucune image reçue'})



def utilisateurs(request):
    error = verify_active_session(request)
    if error:
        return error
    return render(request, 'Utilisateurs.html')



from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

def reset_password_page(request):
    return render(request, "reset_password.html", {"utilisateur_id": request.user.id})

