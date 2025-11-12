# app_eleve/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Eleve


def eleve(request):
    role = request.session.get('role')
    if role not in ['directeur', 'secretaire', 'censeur']:
        return HttpResponseForbidden("Aksè refize.")

    # Récupérer tous les élèves
    eleves = Eleve.objects.all()

    context = {
        'eleves': eleves,
        'role': role,
    }
    return render(request, 'app_eleve/eleve.html', context)