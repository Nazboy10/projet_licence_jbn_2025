# app_note/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.note, name="note"),
    path("api/verifier-eleve/", views.verifier_code_eleve, name="verifier_eleve"),
    path("api/matieres/", views.lister_matieres, name="lister_matieres"),
    path("api/enregistrer-notes/", views.enregistrer_notes, name="enregistrer_notes"),
    path("matieres/gestion/", views.gestion_matieres, name="gestion_matieres"),
    path("api/notes/", views.lister_notes, name="lister_notes"),
]