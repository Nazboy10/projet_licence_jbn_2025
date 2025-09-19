from django.shortcuts import render, redirect
from SGCBA.models import Utilisateur  # Asire modèl ou importé




#view pour dashboard la

def tableau_de_bord(request):
    if 'id' not in request.session:
        return redirect('connexion')  # Si itilizatè pa konekte

    context = {
        'username': request.session['username'],
        'role': request.session['role']
    }
    return render(request, 'tableau_de_bord.html', context)



#vieuws pour Menu an



def Inscription(request):
    return render(request, 'Inscriptions.html')

def Eleve(request):
    return render(request, 'Dossier_Eleves.html')

def Presence(request):
    return render(request, 'Presence.html')

def Note(request):
    return render(request, 'Notes.html')

def Bulletin(request):
    return render(request, 'Bulletin.html')

def Utilisateurs(request):
    return render(request, 'Utilisateurs.html')

def Parametre(request):
    return render(request, 'Parametres.html')