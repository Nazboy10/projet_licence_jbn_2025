from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Presence
from app_inscription.models import Inscription
from app_classe.models import Classe
from app_journal.utils import log_action
from app_eleve.models import Eleve
from SGCBA.utils import verify_active_session

def presence(request):
    role = request.session.get('role')
    if role not in ['directeur', 'secretaire', 'censeur']:
        return HttpResponseForbidden("Aksè refize.")
    
    error = verify_active_session(request)
    if error:
        return error
    
    classes = Classe.objects.all()

    if request.method == "POST":
        code_eleve = request.POST.get('code_eleve')
        date = request.POST.get('date') or str(timezone.now().date())
        statut = request.POST.get('statut', 'present')

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        try:
            eleve_inscription = Inscription.objects.get(code_eleve=code_eleve)
        except Inscription.DoesNotExist:
            error_msg = f"Elèv avèk code '{code_eleve}' pa jwenn."
            if is_ajax:
                return JsonResponse({'success': False, 'error': error_msg}, status=404)
            else:
                messages.error(request, error_msg)
                return redirect('presence')

        # ✅ Vérifier si l'élève est actif
        try:
            eleve = Eleve.objects.get(code_eleve=code_eleve)
            if not eleve.actif:
                error_msg = f"Elèv {eleve.nom} {eleve.prenom} pa aktif. Ou pa kapab anrejistre prensans li."
                if is_ajax:
                    return JsonResponse({'success': False, 'error': error_msg}, status=403)
                else:
                    messages.error(request, error_msg)
                    return redirect('presence')
        except Eleve.DoesNotExist:
            pass  # OK, sera créé plus bas

        # ✅ Définir klas_obj AVANT update_or_create
        klas_obj = None
        if eleve_inscription.classe:
            klas_obj = Classe.objects.filter(
                nom_classe__iexact=eleve_inscription.classe.strip()
            ).first()
            if klas_obj is None:
                print(f"⚠️ Klas '{eleve_inscription.classe}' pa egziste nan tablo Classe.")

        # ✅ Mettre à jour ou créer la présence
        presence_obj, created = Presence.objects.update_or_create(
            eleve=eleve_inscription,
            date=date,
            defaults={
                'klas': klas_obj,
                'statut': statut
            }
        )

        # ✅ Créer dans Eleve si première fois
        if not Eleve.objects.filter(code_eleve=code_eleve).exists():
            Eleve.objects.create(
                code_eleve=eleve_inscription.code_eleve,
                nom=eleve_inscription.nom,
                prenom=eleve_inscription.prenom,
                sexe=eleve_inscription.sexe,
                adresse=eleve_inscription.adresse,
                classe=eleve_inscription.classe,
                telephone=eleve_inscription.telephone,
                nom_tuteur=eleve_inscription.nom_tuteur,
                telephone_tuteur=eleve_inscription.tel_tuteur,
                photo=eleve_inscription.photo,
                actif=True,
                annee_academique=eleve_inscription.annee_academique,
                date_naissance=eleve_inscription.date_naissance,
                email=eleve_inscription.email or '',
                lieu_naissance=eleve_inscription.lieu_naissance or '', 
            )
            extra_msg = " ✅ Elèv la te ajoute nan lis eleve lekol la."
        else:
            extra_msg = ""

        # ✅ Message final
        if created:
            success_msg = f"Presans {eleve_inscription.nom} {eleve_inscription.prenom} te ajoute.{extra_msg}"
        else:
            success_msg = f"Presans {eleve_inscription.nom} {eleve_inscription.prenom} te mete a jou.{extra_msg}"

        if is_ajax:
            log_action(
                request=request,
                action='ajoute',
                objet_type='Presence',
                objet_id=presence_obj.id,
                description=f"Presans ID {presence_obj.id} pou {eleve_inscription.nom} {eleve_inscription.prenom} ({statut}) te ajoute pa {request.session.get('username')}."
            )
            return JsonResponse({'success': True, 'message': success_msg})
        else:
            messages.success(request, success_msg)
            return redirect('presence')
        
    # GET : affichage normal
    from .utils import assurer_presences_jour
    today = timezone.now().date()
    assurer_presences_jour(today)
    presences = Presence.objects.filter(date=today).select_related('eleve', 'klas')
    context = {
        'presences': presences,
        'today': today,
        'role': role,
        'classes': classes,
    }
    return render(request, 'app_presence/presence.html', context)

# Vue pour désactiver

# 👇 Nouvo view pou chache elèv pa code (pou JavaScript)

def get_eleve_by_code(request):
    code = request.GET.get('code', '')
    if code:
        try:
            eleve = Inscription.objects.get(code_eleve=code)
            return JsonResponse({
                'success': True,
                'id': eleve.id,
                'nom': eleve.nom,
                'prenom': eleve.prenom,
                'classe': eleve.classe,
            })
        except Inscription.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Elèv pa jwenn.'})
    return JsonResponse({'success': False, 'error': 'Code vide.'})




# app_presence/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import QRPermanent
from app_classe.models import Classe

def generate_qr_permanent_for_classe(request, classe_id):
    if request.method == "GET":
        classe = get_object_or_404(Classe, id=classe_id)

        # Créer ou récupérer un QR permanent pour cette classe
        qr_obj, created = QRPermanent.objects.get_or_create(classe=classe)

        # Générer l'URL à encoder dans le QR
        qr_url = request.build_absolute_uri(
            reverse('scan_presence_permanent', kwargs={'token': qr_obj.token})
        )

        # ✅ Renvoyer du JSON
        return JsonResponse({
            'success': True,
            'qr_url': qr_url,
            'classe_nom': classe.nom_classe,
            'token': qr_obj.token,
        })

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)










# app_presence/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from app_inscription.models import Inscription
from .models import QRPermanent, Presence
from app_classe.models import Classe
from app_eleve.models import Eleve
import json
from .models import QRPermanent, Presence, NotificationScan  # 👈 Ajoute NotificationScan ici

@csrf_exempt
def scan_presence_permanent(request, token):
    print(f"🔍 Requête reçue pour le token: {token}")

    if request.method == "POST":
        # ✅ Vérifie l'heure
        now = timezone.now()
        # heure_actuelle = now.time()

        #  # Définir les heures autorisées (8h00 à 8h30)
        # debut = now.replace(hour=8, minute=0, second=0, microsecond=0).time()
        # fin = now.replace(hour=8, minute=30, second=0, microsecond=0).time()

        # if not (debut <= heure_actuelle <= fin):
        #       print(f"❌ Hors période autorisée. Heure actuelle: {heure_actuelle}")
        #       return JsonResponse({
        #           'success': False,
        #           'error': f'Scan non autorisé en dehors de la période. Heure actuelle: {heure_actuelle.strftime("%H:%M:%S")}'
        #      }, status=200)

        # print(f"✅ Période autorisée. Heure actuelle: {heure_actuelle}")

        try:
            # Récupérer le QR permanent
            qr_obj = QRPermanent.objects.get(token=token)
            classe = qr_obj.classe
            print(f"✅ QR trouvé pour la classe: {classe.nom_classe}")

            # Récupérer le code_eleve envoyé par l'application mobile
            data = json.loads(request.body)
            code_eleve = data.get('code_eleve')
            print(f"🔍 Code élève reçu: {code_eleve}")

            if not code_eleve:
                print("❌ Code élève manquant dans la requête")
                return JsonResponse({'success': False, 'error': 'Code élève manquant'}, status=200)

            # Vérifier si l'élève existe dans Inscription
            try:
                eleve_inscription = Inscription.objects.get(code_eleve=code_eleve)
                print(f"✅ Élève trouvé: {eleve_inscription.nom} {eleve_inscription.prenom}")
            except Inscription.DoesNotExist:
                print(f"❌ Élève non trouvé avec code: {code_eleve}")
                return JsonResponse({'success': False, 'error': 'Élève non trouvé'}, status=200)

            # ✅ Vérifier si élève est actif (ajouté pour cohérence avec la logique de présence)
            try:
                eleve = Eleve.objects.get(code_eleve=code_eleve)
                if not eleve.actif:
                    print(f"❌ Élève inactif: {eleve.nom} {eleve.prenom}")
                    return JsonResponse({'success': False, 'error': 'Élève inactif'}, status=200)
            except Eleve.DoesNotExist:
                # ✅ Si l'élève n'existe pas encore dans Eleve, c'est OK (il sera créé comme actif)
                pass

            today = now.date()

            # ✅ Mettre à jour ou créer — même si absent, on passe à présent
            presence_obj, created = Presence.objects.update_or_create(
                eleve=eleve_inscription,
                date=today,
                defaults={
                    'klas': classe,
                    'statut': 'present'
                }
            )

            # Optionnel : log si c'était une mise à jour (ex: absent → present)
            if not created:
                print(f"ℹ️ Présence mise à jour pour {eleve_inscription.nom} (était probablement absent)")

            # ✅ Créer une notification de scan (toujours, même si mise à jour)
            # ⚠️ Correction : supprimé le doublon (vous aviez 2 appels identiques)
            NotificationScan.objects.create(
                eleve=eleve_inscription,
                classe=classe
            )

            print(f"✅ Présence enregistrée pour {eleve_inscription.nom} dans la classe {classe.nom_classe}")

            # Si c’est la première fois → créer dans app_eleve
            if not Eleve.objects.filter(code_eleve=code_eleve).exists():
                Eleve.objects.get_or_create(
                    code_eleve=eleve_inscription.code_eleve,
                    defaults={
                        'nom': eleve_inscription.nom,
                        'prenom': eleve_inscription.prenom,
                        'sexe': eleve_inscription.sexe,
                        'adresse': eleve_inscription.adresse,
                        'classe': eleve_inscription.classe,
                        'telephone': eleve_inscription.telephone,
                        'nom_tuteur': eleve_inscription.nom_tuteur,
                        'telephone_tuteur': eleve_inscription.tel_tuteur,
                        'photo': eleve_inscription.photo,
                        'actif': True,
                        'annee_academique': eleve_inscription.annee_academique,
                        'date_naissance': eleve_inscription.date_naissance,
                        'email': eleve_inscription.email or '',
                        'lieu_naissance': eleve_inscription.lieu_naissance or '',
                    }
                )
                print(f"✅ Élève ajouté dans app_eleve: {eleve_inscription.nom}")

            return JsonResponse({'success': True, 'message': 'Présence enregistrée'})

        except QRPermanent.DoesNotExist:
            print(f"❌ QR invalide pour le token: {token}")
            return JsonResponse({'success': False, 'error': 'QR invalide'}, status=200)
        except Exception as e:
            print(f"❌ Erreur serveur: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Erreur serveur'}, status=200)

    print("❌ Méthode non autorisée")
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=200)




# app_presence/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import NotificationScan


def get_notifications_non_lues(request):
    non_lues = NotificationScan.objects.filter(lu=False).count()
    return JsonResponse({'nombre_non_lus': non_lues})


def get_dernieres_notifications(request):
    notifications = NotificationScan.objects.select_related('eleve', 'classe').all()[:10]
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'nom': n.eleve.nom,
            'prenom': n.eleve.prenom,
            'classe': n.classe.nom_classe,
            'date_scan': n.date_scan.strftime('%d/%m/%Y à %H:%M'),
            'lu': n.lu
        })
    return JsonResponse({'notifications': data})





from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import NotificationScan

@csrf_exempt
def mark_notifications_read(request):
    if request.method == "POST":
        # Marquer toutes les notifications non lues comme lues
        NotificationScan.objects.filter(lu=False).update(lu=True)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)