from django.shortcuts import render, redirect
from SGCBA.models import Utilisateur  # Asire modèl ou importé

# view pou splashScreen lan
def splash(request):
    return render(request, 'splash.html')

# view pou dashboard la
def tableau_de_bord(request):
    if 'id' not in request.session:
        return redirect('connexion')  # Si itilizatè pa konekte

    context = {
        'username': request.session['username'],
        'role': request.session['role']
    }
    return render(request, 'tableau_de_bord.html', context)

# views pou meni yo
def inscription(request):
    return render(request, 'inscription.html')

def eleve(request):
    return render(request, 'dossier_eleves.html')

def presence(request):
    return render(request, 'presence.html')

def note(request):
    return render(request, 'notes.html')

def bulletin(request):
    return render(request, 'bulletin.html')

def utilisateurs(request):
    return render(request, 'utilisateurs.html')

def parametre(request):
    return render(request, 'parametres.html')
