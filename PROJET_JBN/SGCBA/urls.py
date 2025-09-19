from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    path('dashboard/', views.tableau_de_bord, name='tableau_de_bord'),
    path("", TemplateView.as_view(template_name="connexion.html"), name="connexion"),
   #urls pou menu yo
    path('inscription/', views.Inscription, name='Inscriptions'),
    path('eleve/', views.Eleve, name='Eleve'),
    path('presence/', views.Presence, name='Presence'),
    path('note/', views.Note, name='Note'),
    path('bulletin/', views.Bulletin, name='Bulletin'),
    path('utilisateurs/', views.Utilisateurs, name='Utilisateurs'),
    path('parametre/', views.Parametre, name='Parametre'),
]
