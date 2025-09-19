# api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UtilisateurViewSet, LoginAPIView
from .views import UtilisateurViewSet

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='api-login'),
]
