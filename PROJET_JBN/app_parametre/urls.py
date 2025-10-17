from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.parametre_view, name='parametre'),
]
