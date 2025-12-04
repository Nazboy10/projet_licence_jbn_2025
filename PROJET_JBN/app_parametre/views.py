# app_parametre/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Parametre
from SGCBA.utils import verify_active_session

def parametre_view(request):
    param = Parametre.load()
    
    error = verify_active_session(request)
    if error:
        return error
    
    if request.method == "POST":
        # Généraux
        param.nom_etablissement = request.POST.get("nom_etablissement", param.nom_etablissement)
        param.annee_academique = request.POST.get("annee_academique", param.annee_academique)
        param.trimestre = int(request.POST.get("trimestre", param.trimestre))
        param.date_debut = request.POST.get("date_debut") or None
        param.date_fin = request.POST.get("date_fin") or None

        if "logo" in request.FILES:
            param.logo = request.FILES["logo"]

        # Académiques
        param.regle_passage = request.POST.get("regle_passage") == "1"

        # Utilisateurs
        param.session_duration = int(request.POST.get("session_duration", param.session_duration))
        param.pw_reset = request.POST.get("pw_reset") == "1"

        # Communication
        param.email_contact = request.POST.get("email_contact", param.email_contact)
        param.tel_contact = request.POST.get("tel_contact", param.tel_contact)

        # Sécurité
        param.backup_auto = request.POST.get("backup_auto") == "1"
        param.logs_active = request.POST.get("logs_active") == "1"

        param.save()
        messages.success(request, "✅ Paramètres enregistrés avec succès !")
        return redirect("parametre")

    return render(request, "app_parametre/parametre.html", {"param": param})