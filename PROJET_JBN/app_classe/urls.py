from django.urls import path
from . import views

urlpatterns = [
    path("", views.classe, name="classe"),
    path('supprimer/<int:id>/', views.supprimer_classe, name='supprimer_classe'),
    path('modifier/<int:id>/', views.modifier_classe, name='modifier_classe'),
]
