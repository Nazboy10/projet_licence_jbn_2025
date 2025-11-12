from django.urls import path
from . import views

urlpatterns = [
    path("", views.presence, name="presence"),
    
    path('get_eleve_by_code/', views.get_eleve_by_code, name='get_eleve_by_code'),  # Nouvo URL
    path('generate-qr-permanent/<int:classe_id>/', views.generate_qr_permanent_for_classe, name='generate_qr_permanent_for_classe'),
    path('scan/permanent/<str:token>/', views.scan_presence_permanent, name='scan_presence_permanent'),
    path('notifications/non-lues/', views.get_notifications_non_lues, name='get_notifications_non_lues'),
    path('notifications/dernieres/', views.get_dernieres_notifications, name='get_dernieres_notifications'),
    path('mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),
    
]
