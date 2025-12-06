# api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UtilisateurViewSet, LoginAPIView
from .views import UploadPhotoAPIView
from .views import ResetPasswordAPIView
from .views import reset_password_confirm_page
from . import views
from api.views import logout_view
  # retire ResetPasswordConfirmAPIView


router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('upload-photo/', UploadPhotoAPIView.as_view(), name='upload-photo'),
    # ✅ Endpoint pour réinitialiser le mot de passe
    path('reset_password/', ResetPasswordAPIView.as_view(), name='api_reset_password'),
    # ✅ Endpoint pour confirmer la réinitialisation (nom unique)
   path('api/reset-password/', ResetPasswordAPIView.as_view(), name='api_reset_password'),
    path('utilisateurs/<int:utilisateur_id>/changer_mot_de_passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),

    # ✅ Page HTML pour confirmer la réinitialisation (nom unique)
    path('reset_password_confirm_page/<uidb64>/<token>/', reset_password_confirm_page, name='reset_password_confirm_page'),
    # ✅ Autres endpoints
    path('inscription/', views.api_ajouter_inscription, name='api_ajouter_inscription'),
    path('login/eleve/', views.login_eleve, name='api_login_eleve'),
    path('logout/', logout_view, name="logout"),
    path('ping/', views.ping_view, name='api_ping'),
    path('utilisateurs/<int:utilisateur_id>/changer_mot_de_passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    
]