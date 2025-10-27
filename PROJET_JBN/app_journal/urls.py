# app_journal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('journal/', views.journal_activite, name='journal_activite'),
]