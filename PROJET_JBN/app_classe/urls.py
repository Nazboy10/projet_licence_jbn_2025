from django.urls import path
from . import views

urlpatterns = [
    path("", views.classe, name="classe"),
    path('ajouter/', views.ajouter_classe_api, name='ajouter_classe_api'),
    path('supprimer/<int:id>/', views.supprimer_classe, name='supprimer_classe'),
    path('modifier/<int:id>/', views.modifier_classe, name='modifier_classe'),
    path('api/eleves/<int:classe_id>/', views.get_eleves_par_classe, name='eleves_par_classe'),
]
