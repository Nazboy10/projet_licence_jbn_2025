# api/views.py
from rest_framework import viewsets
from SGCBA.models import Utilisateur
from .serializers import UtilisateurSerializer


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def get_queryset(self):
        # retire direktè a nan lis la
        return Utilisateur.objects.exclude(role="directeur")
   


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
            return Response(
                {"success": False, "error": "Email et mot de passe requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Utilisateur.objects.get(email=email)

            # 🔒 Tcheke si itilizatè a aktif
            if not user.actif:
                return Response(
                    {"success": False, "error": "Utilisateur désactivé. Contactez l’administration."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # ✅ Verifye mot de pase
            if user.check_password(password):
                # 👉 Mete done user nan session Django
                request.session['id'] = user.id
                request.session['username'] = user.username
                request.session['role'] = user.role

                serializer = UtilisateurSerializer(user)
                return Response(
                    {"success": True, "user": serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"success": False, "error": "Mot de passe incorrect"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Utilisateur.DoesNotExist:
            return Response(
                {"success": False, "error": "Email non trouvé"},
                status=status.HTTP_401_UNAUTHORIZED
            )


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

class UploadPhotoAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        try:
            user = Utilisateur.objects.get(id=user_id)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=404)

        file_obj = request.FILES.get('photo')
        if file_obj:
            user.photo = file_obj
            user.save()
            # retounen URL konplè
            photo_url = request.build_absolute_uri(user.photo.url)
            return Response({"photo_url": photo_url})
        return Response({"error": "Pas de fichier uploadé"}, status=400)
