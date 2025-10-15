from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Inscription
import random
import string
from django.views.decorators.http import require_http_methods


# pou inscriptionyon elev
def inscription(request):
    """Affiche la page avec la liste des élèves"""
    eleves = Inscription.objects.all().order_by('-date_inscription')
    return render(request, "app_inscription/inscription.html", {
        "eleves": eleves,
        "today": timezone.now().date()
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
            "classe": eleve.classe,
            "telephone": eleve.telephone,
            "email": eleve.email,
            "nom_tuteur": eleve.nom_tuteur,
            "tel_tuteur": eleve.tel_tuteur,
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

        # ✅ Récupérer les nouvelles données du formulaire
        nom = request.POST.get("nom", eleve.nom).strip()
        prenom = request.POST.get("prenom", eleve.prenom).strip()
        sexe = request.POST.get("sexe", eleve.sexe).strip()
        adresse = request.POST.get("adresse", eleve.adresse).strip()
        date_naissance = request.POST.get("date_naissance", "")
        classe = request.POST.get("classe", eleve.classe).strip()
        telephone = request.POST.get("telephone", eleve.telephone).strip()
        email = request.POST.get("email", eleve.email).strip()
        nom_tuteur = request.POST.get("nom_tuteur", eleve.nom_tuteur).strip()
        tel_tuteur = request.POST.get("tel_tuteur", eleve.tel_tuteur).strip()

        # ✅ Si gen nouvo foto
        if "photo" in request.FILES:
            eleve.photo = request.FILES["photo"]

        # ✅ Conversion de la date de naissance si fournie
        if date_naissance:
            try:
                eleve.date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d").date()
            except Exception:
                pass  # si format mal, li kite ansyen valè a

        # ✅ Mise à jour des autres champs
        eleve.nom = nom
        eleve.prenom = prenom
        eleve.sexe = sexe
        eleve.adresse = adresse
        eleve.classe = classe
        eleve.telephone = telephone
        eleve.email = email
        eleve.nom_tuteur = nom_tuteur
        eleve.tel_tuteur = tel_tuteur
        eleve.save()

        # ✅ Réponse JSON (pou rafrechi tab la otomatikman sou front-end)
        data = {
            "message": "Inscription modifiée avec succès",
            "id": eleve.id,
            "code_eleve": eleve.code_eleve,
            "nom": eleve.nom,
            "prenom": eleve.prenom,
            "sexe": eleve.sexe,
            "adresse": eleve.adresse,
            "date_naissance": eleve.date_naissance.strftime("%Y-%m-%d") if eleve.date_naissance else "",
            "classe": eleve.classe,
            "telephone": eleve.telephone,
            "email": eleve.email,
            "nom_tuteur": eleve.nom_tuteur,
            "tel_tuteur": eleve.tel_tuteur,
            "photo_url": eleve.photo.url if eleve.photo and hasattr(eleve.photo, "url") else "",
        }
        return JsonResponse(data, status=200)

    except Exception as e:
        print("❌ Erreur lors de la modification :", e)
        return JsonResponse({"error": f"Erreur lors de la modification : {e}"}, status=400)


# pou supprimer yon inskripsyon

@require_http_methods(["DELETE", "POST", "GET"])
def supprimer_inscription(request, id):
    """Supprime une inscription existante"""
    try:
        eleve = get_object_or_404(Inscription, id=id)
        eleve.delete()
        return JsonResponse({"message": "Inscription supprimée avec succès"}, status=200)
    except Exception as e:
        print("❌ Erreur lors de la suppression :", e)
        return JsonResponse({"error": f"Erreur lors de la suppression : {e}"}, status=400)


# pou ajoute yon inskripsyon
@require_POST
def ajouter_inscription(request):
    """Traite l'ajout d'une nouvelle inscription"""
    try:
        nom = request.POST.get("nom", "").strip()
        prenom = request.POST.get("prenom", "").strip()
        sexe = request.POST.get("sexe", "").strip()
        adresse = request.POST.get("adresse", "").strip()
        date_naissance = request.POST.get("date_naissance") or None
        classe = request.POST.get("classe", "").strip()
        telephone = request.POST.get("telephone", "").strip()
        email = request.POST.get("email", "").strip()
        nom_tuteur = request.POST.get("nom_tuteur", "").strip()
        tel_tuteur = request.POST.get("tel_tuteur", "").strip()

        # ✅ Convertir la date de naissance (évite strftime error)
        if date_naissance:
            try:
                date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d").date()
            except Exception:
                date_naissance = None

        # ✅ Date d'inscription
        date_inscription_val = request.POST.get("date_inscription")
        if date_inscription_val:
            try:
                date_inscription = timezone.datetime.strptime(date_inscription_val, "%Y-%m-%d")
                date_inscription = timezone.make_aware(date_inscription) if timezone.is_naive(date_inscription) else date_inscription
            except Exception:
                date_inscription = timezone.now()
        else:
            date_inscription = timezone.now()

        # ✅ Photo (optionnelle)
        photo = request.FILES.get("photo")

        # ✅ Génération du code unique
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

        # ✅ Création de l'élève
        eleve = Inscription.objects.create(
            code_eleve=code_generated,
            nom=nom,
            prenom=prenom,
            sexe=sexe,
            adresse=adresse,
            date_naissance=date_naissance,
            classe=classe,
            telephone=telephone,
            email=email,
            nom_tuteur=nom_tuteur,
            tel_tuteur=tel_tuteur,
            photo=photo,
            date_inscription=date_inscription
        )

        # ✅ Gestion de l'URL de la photo (si existe)
        photo_url = eleve.photo.url if eleve.photo and hasattr(eleve.photo, "url") else ""

        # ✅ Réponse JSON
        data = {
            "id": eleve.id,
            "code_eleve": eleve.code_eleve,
            "nom": eleve.nom,
            "prenom": eleve.prenom,
            "sexe": eleve.sexe,
            "adresse": eleve.adresse,
            "date_naissance": eleve.date_naissance("%Y-%m-%d") if eleve.date_naissance else "",
            "classe": eleve.classe,
            "telephone": eleve.telephone,
            "email": eleve.email,
            "nom_tuteur": eleve.nom_tuteur,
            "tel_tuteur": eleve.tel_tuteur,
            "date_inscription": eleve.date_inscription("%Y-%m-%d"),
            "photo_url": photo_url,
        }
        return JsonResponse(data, status=201)
    

    except Exception as e:
        print("❌ ERREUR DJANGO:", e)
        return JsonResponse({"error": f"Erreur lors de l'inscription : {e}"}, status=400)
