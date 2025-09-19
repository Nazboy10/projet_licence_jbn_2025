# api/views.py
from rest_framework import viewsets
from SGCBA.models import Utilisateur
from .serializers import UtilisateurSerializer

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer


#vieuw pou login via api

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SGCBA.models import Utilisateur
from .serializers import UtilisateurSerializer

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"success": False, "error": "Email et mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Utilisateur.objects.get(email=email)
            if user.check_password(password):
                serializer = UtilisateurSerializer(user)
                return Response({"success": True, "user": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "error": "Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        except Utilisateur.DoesNotExist:
            return Response({"success": False, "error": "Email non trouvé"}, status=status.HTTP_401_UNAUTHORIZED)
