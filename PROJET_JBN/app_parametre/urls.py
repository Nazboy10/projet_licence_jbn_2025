from django.urls import path
from . import views

urlpatterns = [
    path("", views.parametre, name="parametre"),
]
