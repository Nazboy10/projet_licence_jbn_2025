from django.urls import path
from . import views
from .views import total_eleves

urlpatterns = [
    path("", views.eleve, name="eleve"),
    path('toggle-actif/<int:id>/', views.toggle_actif_eleve, name='toggle_actif_eleve'),
    path('details/<int:id>/', views.eleve_details, name='eleve_details'),
    path('modifier/<int:id>/', views.modifier_eleve, name='modifier_eleve'),
     path('total-eleves/', total_eleves, name='total_eleves'),
    
]
