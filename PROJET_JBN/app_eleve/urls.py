from django.urls import path
from . import views

urlpatterns = [
    path("", views.eleve, name="eleve"),
    
]
