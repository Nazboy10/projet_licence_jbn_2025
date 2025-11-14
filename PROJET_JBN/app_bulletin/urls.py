# app_bulletin/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.bulletin, name="bulletin"),
    path("api/bulletin/", views.api_bulletin_eleve, name="api_bulletin_eleve"),
    path("api/enregistrer/", views.api_enregistrer_bulletin, name="api_enregistrer_bulletin"),
    path("api/liste_eleves/", views.api_liste_eleves_pour_bulletin, name="api_liste_eleves_bulletin"),
]