# api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UtilisateurViewSet, LoginAPIView
from .views import UploadPhotoAPIView
from .views import ResetPasswordAPIView, ResetPasswordConfirmAPIView
from .views import reset_password_confirm_page
from . import views
from api.views import logout_view

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('upload-photo/', UploadPhotoAPIView.as_view(), name='upload-photo'),
    # ✅ Endpoint pour réinitialiser le mot de passe
    path('reset_password/', ResetPasswordAPIView.as_view(), name='api_reset_password'),
    # ✅ Endpoint pour confirmer la réinitialisation (nom unique)
    path('reset_password_confirm/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='api_reset_password_confirm'),
    # ✅ Page HTML pour confirmer la réinitialisation (nom unique)
    path('reset_password_confirm_page/<uidb64>/<token>/', reset_password_confirm_page, name='reset_password_confirm_page'),
    # ✅ Autres endpoints
    path('inscription/', views.api_ajouter_inscription, name='api_ajouter_inscription'),
    path('login/eleve/', views.login_eleve, name='api_login_eleve'),
    path('logout/', logout_view, name="logout"),
    path('ping/', views.ping_view, name='api_ping'),
]