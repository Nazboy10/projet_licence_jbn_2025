from django.urls import path
from django.views.generic import TemplateView
from . import views
from api.views import reset_password_page
from api.views import reset_password_confirm_page

urlpatterns = [
    path("", views.splash, name='splash'),
    path('connexion/', TemplateView.as_view(template_name="connexion.html"), name="connexion"),
    path('dashboard/', views.tableau_de_bord, name='tableau_de_bord'),
    path('inscription/', views.Inscription, name='Inscriptions'),
    path('eleve/', views.Eleve, name='Eleve'),
    path('presence/', views.Presence, name='Presence'),
    path('note/', views.Note, name='Note'),
    path('bulletin/', views.Bulletin, name='Bulletin'),
    path('utilisateurs/', views.Utilisateurs, name='Utilisateurs'),
    path('parametre/', views.Parametre, name='Parametre'),
    path('reset_password/', reset_password_page, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', reset_password_confirm_page, name='reset_password_confirm'),
    
]
