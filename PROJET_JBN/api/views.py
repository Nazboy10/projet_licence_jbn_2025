# api/views.py
from rest_framework import viewsets
from SGCBA.models import Utilisateur
from .serializers import UtilisateurSerializer
from .permissions import IsDirecteur
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from app_journal.utils import log_action


class IsLoggedIn(BasePermission):
    """
    Verifye ke itilizatè a gen sesyon aktif
    """
    def has_permission(self, request, view):
        return request.session.get('id') is not None


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def get_queryset(self):
        # retire direktè a nan lis la
        return Utilisateur.objects.exclude(role="directeur")
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsDirecteur()]
        # itilize session olye de IsAuthenticated
        return [IsLoggedIn()]
    

    # ✅ Nouvo metòd create avèk tracabilite
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # ✅ Kenbe enstans itilizatè a

        # ✅ Kenbe aksyon an
        log_action(
            request=request,
            action='ajoute',
            objet_type='Utilisateur',
            objet_id=user.id,
            description=f"Itilizatè ID {user.id} ({user.username}) te ajoute pa {request.session.get('username')}."
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # ✅ Nouvo metòd update avèk tracabilite
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # ✅ Kenbe valè avan pou deskripsyon
        old_username = instance.username
        old_role = instance.role
        old_actif = instance.actif

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # ✅ Kenbe enstans itilizatè a

        # ✅ Kenbe aksyon an
        log_action(
            request=request,
            action='modifye',
            objet_type='Utilisateur',
            objet_id=user.id,
            description=f"Itilizatè ID {user.id} te modifye pa {request.session.get('username')}. Avan: {old_username} ({old_role}), Kounye: {user.username} ({user.role})."
        )

        return Response(serializer.data)

    # ✅ Nouvo metòd destroy avèk tracabilite
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # ✅ Kenbe aksyon an avan efase
        log_action(
            request=request,
            action='efase',
            objet_type='Utilisateur',
            objet_id=instance.id,
            description=f"Itilizatè ID {instance.id} ({instance.username}) te efase pa {request.session.get('username')}."
        )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


#vieuw pou login via api

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SGCBA.models import Utilisateur
from .serializers import UtilisateurSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from SGCBA.models import Utilisateur
from .serializers import UtilisateurSerializer
class LoginAPIView(APIView):
    """
    Login via API, retounen done itilizatè + token, verifye si deja konekte.
    """
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

            if not user.actif:
                return Response(
                    {"success": False, "error": "Utilisateur désactivé. Contactez l’administration."},
                    status=status.HTTP_403_FORBIDDEN
                )

            if user.check_password(password):

                # ✅ Si itilizatè a deja gen token, li deja konekte
                if user.token:
                    return Response(
                        {"success": False, "error": "Utilisateur déjà connecté"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Kreye token pou premye fwa
                token = user.generate_token()

                # Kenbe session Django
                request.session['id'] = user.id
                request.session['username'] = user.username
                request.session['role'] = user.role

                serializer = UtilisateurSerializer(user)
                return Response(
                    {"success": True, "user": serializer.data, "token": token},
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



















# # app_api/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.dateparse import parse_date
import json
import random
import string
from app_inscription.models import Inscription
from app_parametre.models import Parametre
import base64
from django.core.files.base import ContentFile

@csrf_exempt
def api_ajouter_inscription(request):
    if request.method != "POST":
         return JsonResponse({
            "success": False,
            "error_code": "method_not_allowed",
            "error": "Méthode non autorisée"
        }, status=405)
    
    if request.content_type != "application/json":
        return JsonResponse({
    "success": False,
    "error_code": "invalid_content_type",
    "error": "Content-Type doit être application/json"
}, status=400)

    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
       return JsonResponse({
    "success": False,
    "error_code": "invalid_json",
    "error": "JSON invalide"
}, status=400)

    try:
        # Ektrè done yo
        nom = data.get("nom", "").strip()
        prenom = data.get("prenom", "").strip()
        sexe = data.get("sexe", "").strip()
        adresse = data.get("adresse", "").strip()
        date_naissance_str = data.get("date_naissance")
        classe = data.get("classe", "").strip()
        telephone = data.get("telephone", "").strip()
        email = data.get("email", "").strip().lower()
        nom_tuteur = data.get("nom_tuteur", "").strip()
        tel_tuteur = data.get("tel_tuteur", "").strip()
        date_inscription_str = data.get("date_inscription")

        # Validasyon chan obligatwa
        if not all([nom, prenom, sexe, adresse, classe, telephone]):
           return JsonResponse({
    "success": False,
    "error_code": "missing_fields",
    "error": "Tous les champs obligatoires doivent être remplis."
}, status=400)

        # ✅ Verifye email
        if email and Inscription.objects.filter(email__iexact=email).exists():
            return JsonResponse({
    "success": False,
    "error_code": "email_exists",
    "error": f"L'email {email} est déjà utilisé."
}, status=400)

        # ✅ Verifye telephone
        if Inscription.objects.filter(telephone=telephone).exists():
            return JsonResponse({
    "success": False,
    "error_code": "phone_exists",
    "error": f"Le téléphone {telephone} est déjà utilisé."
}, status=400)

        # 🔥 Dat nesans
        date_naissance = None
        if date_naissance_str:
            date_naissance = parse_date(date_naissance_str)
            if not date_naissance:
               return JsonResponse({
    "success": False,
    "error_code": "invalid_date_naissance",
    "error": "Format date de naissance invalide. Utilisez AAAA-MM-JJ."
}, status=400)

        # 🔥 Dat enskripsyon
        if not date_inscription_str:
            return JsonResponse({
    "success": False,
    "error_code": "missing_date_inscription",
    "error": "La date d'inscription est requise."
}, status=400)
        
        date_inscription_date = parse_date(date_inscription_str)
        if not date_inscription_date:
           return JsonResponse({
    "success": False,
    "error_code": "invalid_date_inscription",
    "error": "Format date d'inscription invalide. Utilisez AAAA-MM-JJ."
}, status=400)

        # 🔒 Verifye peryod akademik
        param = Parametre.load()
        if param.date_debut and param.date_fin:
            if not (param.date_debut <= date_inscription_date <= param.date_fin):
               return JsonResponse({
    "success": False,
    "error_code": "date_out_of_range",
    "error": f"La date d'inscription doit être entre {param.date_debut} et {param.date_fin}."
}, status=400)
    
         
         

        # ⚙️ Genere kòd elèv
        def generate_code_eleve(nom, prenom, sexe):
            n = (nom[0] if nom else "X").upper()
            p = (prenom[0] if prenom else "X").upper()
            s = (sexe[0] if sexe else "X").upper()
            while True:
                letters = ''.join(random.choices(string.ascii_uppercase, k=3))
                numbers = random.randint(100, 999)
                prefix = f"{n}{p}{s}{letters}-{numbers}"
                if not Inscription.objects.filter(code_eleve=prefix).exists():
                    return prefix

        code_generated = generate_code_eleve(nom, prenom, sexe)

       # 📸 Gestion de la photo (si fournie en base64)
        photo = None
        photo_data = data.get("photo")
        if photo_data:
            try:
                # Format attendu: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
                if photo_data.startswith("data:image"):
                    format, imgstr = photo_data.split(";base64,")
                    ext = format.split("/")[-1]  # Récupère "jpeg", "png", etc.
                    photo = ContentFile(base64.b64decode(imgstr), name=f"eleve_{code_generated}.{ext}")
            except Exception as e:
                print("❌ Erreur décodage photo:", e)



        # 💾 Kreye elèv la
        from django.utils import timezone as tz
        date_inscription = tz.make_aware(
            tz.datetime.combine(date_inscription_date, tz.datetime.min.time())
        )

        eleve = Inscription.objects.create(
            code_eleve=code_generated,
            nom=nom,
            prenom=prenom,
            sexe=sexe,
            adresse=adresse,
            annee_academique=param.annee_academique,
            date_naissance=date_naissance,
            classe=classe,
            telephone=telephone,
            email=email,
            nom_tuteur=nom_tuteur,
            tel_tuteur=tel_tuteur,
            date_inscription=date_inscription,
            photo=photo
        )

        # ✅ Repons siksè
        return JsonResponse({
            "success": True,
            "message": "Inscription réussie",
            "eleve": {
                "id": eleve.id,
                "code_eleve": eleve.code_eleve,
                "nom": eleve.nom,
                "prenom": eleve.prenom,
                "sexe": eleve.sexe,
                "adresse": eleve.adresse,
                "date_naissance": eleve.date_naissance.strftime("%Y-%m-%d") if eleve.date_naissance else None,
                "classe": eleve.classe,
                "telephone": eleve.telephone,
                "email": eleve.email,
                "nom_tuteur": eleve.nom_tuteur,
                "tel_tuteur": eleve.tel_tuteur,
                "date_inscription": eleve.date_inscription.strftime("%Y-%m-%d"),
                "annee_academique": eleve.annee_academique,
                "photo_url": request.build_absolute_uri(eleve.photo.url) if eleve.photo else None
            }
        }, status=201)

    except Exception as e:
     print("❌ Erreur API inscription mobile:", e)
    return JsonResponse({
        "success": False,
        "error_code": "server_error",
        "error": "Erreur interne du serveur"
    }, status=500)







# api/views.py pour eleve connecter
from django.conf import settings
from urllib.parse import urljoin
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_inscription.models import Inscription

logger = logging.getLogger(__name__)

@csrf_exempt
def login_eleve(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)

    if request.content_type != 'application/json':
        return JsonResponse({'success': False, 'error': 'Le format doit être JSON'}, status=400)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'success': False, 'error': 'Données non valides'}, status=400)

    code_eleve = data.get('code_eleve')
    nom_complet = data.get('nom_complet')

    if not code_eleve or not isinstance(code_eleve, str) or not code_eleve.strip():
        return JsonResponse({'success': False, 'error': 'Code élève manquant ou invalide'}, status=400)

    if not nom_complet or not isinstance(nom_complet, str) or not nom_complet.strip():
        return JsonResponse({'success': False, 'error': 'Nom complet manquant'}, status=400)

    nom_complet = nom_complet.strip()
    parts = nom_complet.split(' ', 1)
    if len(parts) < 2:
        return JsonResponse({'success': False, 'error': 'Veuillez entrer votre nom et prénom'}, status=400)

    nom, prenom = parts[0].strip(), parts[1].strip()
    if not nom or not prenom:
        return JsonResponse({'success': False, 'error': 'Nom ou prénom vide'}, status=400)

    # ✅ Recherche de l'élève
    try:
        eleve = Inscription.objects.get(
            code_eleve=code_eleve.strip(),
            nom__iexact=nom,
            prenom__iexact=prenom,
            valide=True
        )
    except Inscription.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Code ou nom incorrect'}, status=400)

    # ✅ Définir photo_url APRES le try/except
    photo_url = None
    if eleve.photo:
        base_url = request.build_absolute_uri('/')
        photo_url = urljoin(base_url, eleve.photo.url)

    return JsonResponse({
        'success': True,
       'eleve': {
            'id': eleve.id,
            'nom': eleve.nom,
            'prenom': eleve.prenom,
            'code_eleve': eleve.code_eleve,
            'sexe': eleve.sexe,
            'adresse': eleve.adresse,
            'annee_academique': eleve.annee_academique or "",
            'date_naissance': eleve.date_naissance,
            'classe': eleve.classe,
            'telephone': eleve.telephone,
            'email': eleve.email or "",
            'nom_tuteur': eleve.nom_tuteur,
            'tel_tuteur': eleve.tel_tuteur,
            'photo_url': photo_url,
        }
    })