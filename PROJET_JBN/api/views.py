# api/views.py
from rest_framework import viewsets
from SGCBA.models import Utilisateur
from .serializers import UtilisateurSerializer
from .permissions import IsDirecteur
from rest_framework.permissions import IsAuthenticated


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def get_queryset(self):
        # retire direktè a nan lis la
        return Utilisateur.objects.exclude(role="directeur")
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsDirecteur()]
        return [IsAuthenticated()]
   


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





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from SGCBA.models import Utilisateur
from .tokens import custom_token_generator

class ResetPasswordAPIView(APIView):
    """
    Voye imel reset password ak token
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"success": False, "error": "Email requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            return Response({"success": False, "error": "Email non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = custom_token_generator.make_token(user)

        # Lyen frontend pou reset password
       # api/views.py
       # api/views.py
        # api/views.py
        reset_link = f"http://localhost:8000/reset_password_confirm/{uid}/{token}/"



        # Imel
        subject = "Réinitialisation du mot de passe"
        message = f"Bonjour {user.nom},\n\nCliquez sur ce lien pour réinitialiser votre mot de passe:\n{reset_link}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response({"success": True, "message": "Email de réinitialisation envoyé"}, status=status.HTTP_200_OK)














class ResetPasswordConfirmAPIView(APIView):
    """
    Verifye token epi mete nouvo modpas
    """
    def post(self, request, uidb64, token):
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if not password or not password2:
            return Response(
                {"success": False, "error": "Tous les champs sont requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != password2:
            return Response(
                {"success": False, "error": "Les mots de passe ne correspondent pas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Utilisateur.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
            return Response(
                {"success": False, "error": "Lien invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ verifye validite token la
        if not custom_token_generator.check_token(user, token):
            return Response(
                {"success": False, "error": "Lien expiré ou invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ mete nouvo modpas
        user.set_password(password)
        user.save()
        return Response(
            {"success": True, "message": "Mot de passe changé avec succès"},
            status=status.HTTP_200_OK
        )





# api/views.py
from django.shortcuts import render

def reset_password_page(request):
    return render(request, 'reset_password.html')  # template ou deja genyen


def reset_password_confirm_page(request, uidb64, token):
    return render(request, 'reset_password_confirm.html')

# paj HTML
def reset_password_confirm_page(request, uidb64, token):
    return render(request, 'reset_password_confirm.html', {
        'uidb64': uidb64,
        'token': token
    })

