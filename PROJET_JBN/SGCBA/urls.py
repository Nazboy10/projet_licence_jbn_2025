from django.urls import path
from django.views.generic import TemplateView
from . import views
from api.views import reset_password_page, reset_password_confirm_page

urlpatterns = [
    path("", views.splash, name='splash'),
   path('connexion/', views.connexion, name="connexion"),
    path('dashboard/', views.tableau_de_bord, name='tableau_de_bord'),
    # path('inscription/', views.Inscription, name='inscription'),
    # path('eleve/', views.eleve, name='eleve'),
    # path('presence/', views.presence, name='presence'),
    # path('note/', views.note, name='note'),
    # path('bulletin/', views.bulletin, name='bulletin'),
    path('utilisateurs/', views.utilisateurs, name='utilisateurs'),
    
    path('reset_password/', reset_password_page, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', reset_password_confirm_page, name='reset_password_confirm'),
    path('changer-photo/', views.changer_photo, name='changer_photo'),

]
