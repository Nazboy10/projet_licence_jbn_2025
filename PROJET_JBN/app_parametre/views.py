from django.shortcuts import render

def parametre(request):
    return render(request, "app_parametre/parametre.html")
