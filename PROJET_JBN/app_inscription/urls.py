from django.urls import path
from . import views

urlpatterns = [
    path('', views.inscription, name='inscription'),
    path('ajouter/', views.ajouter_inscription, name='ajouter_inscription'),
    path('modifier/<int:id>/', views.modifier_inscription, name='modifier_inscription'),
    path('supprimer/<int:id>/', views.supprimer_inscription, name='supprimer_inscription'),
    path('get/<int:id>/', views.get_inscription, name='get_inscription'),  # 🆕 Ajoute sa
]



