from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Inscription
import random
import string
from django.views.decorators.http import require_http_methods
from app_parametre.models import Parametre
from app_parametre.models import Parametre
from SGCBA.utils import verify_active_session
from app_classe.models import Classe
# pou inscriptionyon elev
from datetime import date, timedelta
from app_journal.utils import log_action  # Importe fonksyon tracabilite a

def inscription(request):
     # Verifye si itilizatè a konekte (selon sesyon ou)
    error = verify_active_session(request)
    if error:
        return error  # oswa return HttpResponseForbidden("Aksè refize")
   # ✅ Bon
    classes = Classe.objects.all().order_by('nom_classe')
    today = date.today()
    # Elèv dwe gen pou pi piti 10 an → nes pi vit 10 an avan jodi a
    MIN_AGE = 11
    max_birth_date = today.replace(year=today.year - MIN_AGE)
    role = request.session.get('role', None)
    # Ajuste pou ane bisextil (si 29 fevri)
    try:
        max_birth_date = today.replace(year=today.year - MIN_AGE)
    except ValueError:
        # Si jodi a se 29 fevri epi ane kible a pa bisextil
        max_birth_date = today.replace(year=today.year - MIN_AGE, day=28)

    eleves = Inscription.objects.all().order_by('-date_inscription')
    param = Parametre.load()
    return render(request, "app_inscription/inscription.html", {
        "eleves": eleves,
        "today": today,
        "max_birth_date": max_birth_date,  # <-- nouvo valè
        "annee_academique": param.annee_academique,
        'classes': classes,
        'role': role,
    })
# 📌 Pèmèt chaje done yon elèv nan modal "modifier"
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_inscription(request, id):
    """Renvwaye done yon elèv an JSON pou modal modification"""
    try:
        eleve = get_object_or_404(Inscription, id=id)
        data = {
            "id": eleve.id,
            "code_eleve": eleve.code_eleve,
            "nom": eleve.nom,
            "prenom": eleve.prenom,
            "sexe": eleve.sexe,
            "adresse": eleve.adresse,
            "date_naissance": eleve.date_naissance.strftime("%Y-%m-%d") if eleve.date_naissance else "",
            "lieu_naissance": eleve.lieu_naissance, 
            "classe": eleve.classe,
            "telephone": eleve.telephone,
            "email": eleve.email,
            "nom_tuteur": eleve.nom_tuteur,
            "tel_tuteur": eleve.tel_tuteur,
             "date_inscription": eleve.date_inscription,
            "photo_url": eleve.photo.url if eleve.photo and hasattr(eleve.photo, "url") else "",
        }
        return JsonResponse(data, status=200)
    except Exception as e:
        print("❌ Erreur chargement élève:", e)
        return JsonResponse({"error": f"Erreur lors du chargement : {e}"}, status=400)

# pou modifye yon inskripsyon

@require_http_methods(["POST"])
def modifier_inscription(request, id):
    """Modifie une inscription existante"""
    try:
        eleve = get_object_or_404(Inscription, id=id)

        nom = request.POST.get("nom", eleve.nom).strip()
        prenom = request.POST.get("prenom", eleve.prenom).strip()
        sexe = request.POST.get("sexe", eleve.sexe).strip()
        adresse = request.POST.get("adresse", eleve.adresse).strip()
        date_naissance = request.POST.get("date_naissance", "")
        lieu_naissance = request.POST.get("lieu_naissance", "").strip()
        classe = request.POST.get("classe", eleve.classe).strip()
        telephone = request.POST.get("telephone", eleve.telephone).strip()
        email = request.POST.get("email", eleve.email).strip().lower()  # normalize email
        nom_tuteur = request.POST.get("nom_tuteur", eleve.nom_tuteur).strip()
        tel_tuteur = request.POST.get("tel_tuteur", eleve.tel_tuteur).strip()


        # ✅ Vérifier si l'email existe déjà pour un autre élève
        if Inscription.objects.filter(email__iexact=email).exclude(id=eleve.id).exists():
            return JsonResponse({"error": f"L'email {email} est déjà utilisé par un autre élève."}, status=400)
        
        # ✅ Vérifier téléphone
        if telephone and Inscription.objects.filter(telephone=telephone).exclude(id=eleve.id).exists():
            return JsonResponse({"error": f"Le numéro de téléphone {telephone} est déjà utilisé par un autre élève."}, status=400)


        if "photo" in request.FILES:
            eleve.photo = request.FILES["photo"]

        if date_naissance:
            try:
                eleve.date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d").date()
            except Exception:
                pass

        # Mise à jour des autres champs
        eleve.nom = nom
        eleve.prenom = prenom
        eleve.sexe = sexe
        eleve.date_naissance = date_naissance
        eleve.lieu_naissance = lieu_naissance 
        eleve.adresse = adresse
        eleve.classe = classe
        eleve.telephone = telephone
        eleve.email = email
        eleve.nom_tuteur = nom_tuteur
        eleve.tel_tuteur = tel_tuteur
        eleve.save()

        data = {
            "message": "Inscription modifiée avec succès",
            "id": eleve.id,
            "code_eleve": eleve.code_eleve,
            "nom": eleve.nom,
            "prenom": eleve.prenom,
            "sexe": eleve.sexe,
            "adresse": eleve.adresse,
            "date_naissance": eleve.date_naissance.strftime("%Y-%m-%d") if eleve.date_naissance else "",
             "lieu_naissance": eleve.lieu_naissance,
            "classe": eleve.classe,
            "telephone": eleve.telephone,
            "email": eleve.email,
            "nom_tuteur": eleve.nom_tuteur,
            "tel_tuteur": eleve.tel_tuteur,
            "photo_url": eleve.photo.url if eleve.photo and hasattr(eleve.photo, "url") else "",
        }

        log_action(
        request=request,
        action='modifye',
        objet_type='Inscription',
        objet_id=eleve.id,
        description=f"Inskripsyon pou {eleve.nom} {eleve.prenom} te ajoute pa {request.session.get('username')}."
    )

        return JsonResponse(data, status=200)

    except Exception as e:
        print("❌ Erreur lors de la modification :", e)
        return JsonResponse({"error": "Une erreur est survenue lors de la modification."}, status=400)


# pou supprimer yon inskripsyon

@require_http_methods(["DELETE", "POST", "GET"])
def supprimer_inscription(request, id):
    """Supprime une inscription existante"""
    try:
        eleve = get_object_or_404(Inscription, id=id)
        eleve.delete()
       
        log_action(
        request=request,
        action='efase',
        objet_type='Inscription',
        objet_id=eleve.id,
        description=f"Inskripsyon pou {eleve.nom} {eleve.prenom} te ajoute pa {request.session.get('username')}."
    )

        return JsonResponse({"message": "Inscription supprimée avec succès"}, status=200)
    except Exception as e:
        print("❌ Erreur lors de la suppression :", e)
        return JsonResponse({"error": f"Erreur lors de la suppression : {e}"}, status=400)


# pou ajoute yon inskripsyon
@require_POST
def ajouter_inscription(request):
   
    param = Parametre.load()

    # Récupérer la date choisie par l'utilisateur
    date_inscription_str = request.POST.get("date_inscription")
    if not date_inscription_str:
        return JsonResponse({"error": "La date d'inscription est requise."}, status=400)

    try:
        date_inscription_date = datetime.strptime(date_inscription_str, "%Y-%m-%d").date()
    except Exception:
        return JsonResponse({"error": "Format de date invalide."}, status=400)

    # Vérifier qu'elle est dans la période académique
    if param.date_debut and param.date_fin:
        if not (param.date_debut <= date_inscription_date <= param.date_fin):
            return JsonResponse({
                "error": f"La date d'inscription doit être entre {param.date_debut} et {param.date_fin}."
            }, status=400)

    """Traite l'ajout d'une nouvelle inscription"""
    try:
        nom = request.POST.get("nom", "").strip()
        prenom = request.POST.get("prenom", "").strip()
        sexe = request.POST.get("sexe", "").strip()
        adresse = request.POST.get("adresse", "").strip()
        date_naissance = request.POST.get("date_naissance") or None
        lieu_naissance = request.POST.get("lieu_naissance", "").strip()
        classe = request.POST.get("classe", "").strip()
        telephone = request.POST.get("telephone", "").strip()
        email = request.POST.get("email", "").strip()
        nom_tuteur = request.POST.get("nom_tuteur", "").strip()
        tel_tuteur = request.POST.get("tel_tuteur", "").strip()

        # ✅ Vérifier si l'email existe déjà
        if Inscription.objects.filter(email=email).exists():
            return JsonResponse({"error": f"L'email {email} est déjà utilisé."}, status=400)

        # ✅ Vérifier si le téléphone existe déjà
        if telephone and Inscription.objects.filter(telephone=telephone).exists():
          return JsonResponse({"error": f"Le numéro de téléphone {telephone} est déjà utilisé."}, status=400)    

        # Conversion de la date de naissance
        if date_naissance:
            try:
                date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d").date()
            except Exception:
                date_naissance = None

        # Date d'inscription
          # 🔥 DATE D'INSCRIPTION : sèlman dat chwazi a, pa gen default
        date_inscription_str = request.POST.get("date_inscription")
        if not date_inscription_str:
            return JsonResponse({"error": "La date d'inscription est requise."}, status=400)

        try:
            # Konvèti chenn an an dat (sèlman dat)
            date_only = datetime.strptime(date_inscription_str, "%Y-%m-%d").date()
            # Kòmanse jounen an (00:00:00) epi fè li "aware"
            date_inscription = timezone.make_aware(
                timezone.datetime.combine(date_only, timezone.datetime.min.time())
            )
        except Exception:
            return JsonResponse({"error": "Format de date invalide."}, status=400)

        # Photo optionnelle
        photo = request.FILES.get("photo")

        # Génération du code unique
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

        # Création de l'élève
        eleve = Inscription.objects.create(
            code_eleve=code_generated,
            nom=nom,
            prenom=prenom,
            sexe=sexe,
            adresse=adresse,
            annee_academique=param.annee_academique,
            date_naissance=date_naissance,
            lieu_naissance=lieu_naissance,
            classe=classe,
            telephone=telephone,
            email=email,
            nom_tuteur=nom_tuteur,
            tel_tuteur=tel_tuteur,
            photo=photo,
            date_inscription=date_inscription,
            valide=False,
            
        )

        # Gestion URL photo
        photo_url = eleve.photo.url if eleve.photo and hasattr(eleve.photo, "url") else ""

        # Réponse JSON
        data = {
            "id": eleve.id,
            "code_eleve": eleve.code_eleve,
            "nom": eleve.nom,
            "prenom": eleve.prenom,
            "sexe": eleve.sexe,
            "adresse": eleve.adresse,
            "date_naissance": eleve.date_naissance.strftime("%Y-%m-%d") if eleve.date_naissance else "",
            "lieu_naissance": eleve.lieu_naissance,
            "classe": eleve.classe,
            "telephone": eleve.telephone,
            "email": eleve.email,
            "nom_tuteur": eleve.nom_tuteur,
            "tel_tuteur": eleve.tel_tuteur,
            "date_inscription": eleve.date_inscription.strftime("%Y-%m-%d") if eleve.date_inscription else "",
            "photo_url": photo_url,
            
        }
         
        log_action(
        request=request,
        action='ajoute',
        objet_type='Inscription',
        objet_id=eleve.id,
        description=f"Inskripsyon pou {eleve.nom} {eleve.prenom} te ajoute pa {request.session.get('username')}."
    )


        return JsonResponse(data, status=201)

    except Exception as e:
        print("❌ ERREUR DJANGO:", e)
        return JsonResponse({"error": "Une erreur est survenue lors de l'inscription."}, status=400)


from django.db import models
# pour rechercher_inscription
def rechercher_inscription(request):
    """Renvoie les élèves filtrés en JSON (pour recherche AJAX)"""
    query = request.GET.get('q', '').strip()
    eleves = Inscription.objects.all()

    if query:
        eleves = eleves.filter(
            models.Q(nom__icontains=query) |
            models.Q(prenom__icontains=query) |
            models.Q(code_eleve__icontains=query) |
            models.Q(classe__icontains=query) |
            models.Q(telephone__icontains=query) |
            models.Q(email__icontains=query)
        )

    eleves = eleves.order_by('-date_inscription')

    results = []
    for e in eleves:
        results.append({
            "id": e.id,
            "code_eleve": e.code_eleve,
            "nom": e.nom,
            "prenom": e.prenom,
            "sexe": e.sexe,
            "adresse": e.adresse,
            "date_naissance": e.date_naissance.strftime("%Y-%m-%d") if e.date_naissance else "",
            "classe": e.classe,
            "telephone": e.telephone,
            "email": e.email,
            "nom_tuteur": e.nom_tuteur,
            "tel_tuteur": e.tel_tuteur,
            "date_inscription": e.date_inscription.strftime("%Y-%m-%d"),
            "photo_url": e.photo.url if e.photo else "/static/images/default.png",
        })

    return JsonResponse({"eleves": results}, safe=False)





# app_inscription/views.py
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def valider_inscription(request, id):
    if request.method == "POST":
        eleve = get_object_or_404(Inscription, id=id)

        if eleve.valide:
            return JsonResponse({'success': False, 'error': 'Déjà validé.'})

        # ✅ Nettoyer l'email (retire espas)
        if eleve.email:
            eleve.email = eleve.email.strip().lower()
        
        # ✅ Vérifier que l'email existe et est valide
        if not eleve.email:
            return JsonResponse({
                'success': False,
                'error': 'Email manquant. Validation impossible sans email.'
            })
        
        # ✅ Validation plus stricte de l'email
        try:
            validate_email(eleve.email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'error': f'Email invalide: {eleve.email}. Veuillez corriger l\'adresse email.'
            })
        
        # ✅ Vérification supplémentaire du format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, eleve.email):
            return JsonResponse({
                'success': False,
                'error': f'Format d\'email incorrect: {eleve.email}'
            })

        # Valider l'inscription
        eleve.valide = True
        eleve.save()

        # Préparer l'email
        sujet = "Votre inscription a été validée"
        message = f"""
Bonjour {eleve.prenom} {eleve.nom},

Votre inscription a été validée avec succès.

Votre code élève est : {eleve.code_eleve}

Utilisez ce code pour vous connecter dans l'application mobile.

Merci !
        """.strip()

        try:
            # ✅ S'assurer que l'email est une liste propre
            destinataires = [eleve.email.strip()]
            
            send_mail(
                sujet,
                message,
                settings.DEFAULT_FROM_EMAIL,
                destinataires,
                fail_silently=False,  # Pour voir l'erreur complète
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Validé et email envoyé à {eleve.email}'
            })
            
        except Exception as e:
            # ✅ Log détaillé de l'erreur
            print(f"Erreur d'envoi d'email détaillée:")
            print(f"  - Email destinataire: '{eleve.email}'")
            print(f"  - Type d'erreur: {type(e).__name__}")
            print(f"  - Message: {str(e)}")
            
            return JsonResponse({
                'success': False,
                'error': f'Échec de l\'envoi de l\'email: {str(e)}'
            })

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})