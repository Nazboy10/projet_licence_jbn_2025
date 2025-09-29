# api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UtilisateurViewSet, LoginAPIView
from .views import UtilisateurViewSet
from .views import UploadPhotoAPIView
from .views import ResetPasswordAPIView, ResetPasswordConfirmAPIView
from .views import reset_password_confirm_page

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('upload-photo/', UploadPhotoAPIView.as_view(), name='upload-photo'),
    path('reset_password/', ResetPasswordAPIView.as_view(), name='api_reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='api_reset_password_confirm'),
    path('api/reset_password_confirm/<uidb64>/<token>/', ResetPasswordConfirmAPIView.as_view(), name='api_reset_password_confirm'),
     path('reset_password_confirm/<uidb64>/<token>/', reset_password_confirm_page, name='reset_password_confirm_page'),
]
