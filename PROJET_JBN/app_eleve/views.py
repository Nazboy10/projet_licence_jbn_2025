from django.shortcuts import render

def eleve(request):
    return render(request, "app_eleve/eleve.html")
