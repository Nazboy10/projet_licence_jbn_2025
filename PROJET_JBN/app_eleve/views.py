# app_eleve/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Eleve
from SGCBA.utils import verify_active_session

# app_eleve/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q  # ← Pour la recherche
from .models import Eleve
from SGCBA.utils import verify_active_session

def eleve(request):
    role = request.session.get('role')
    if role not in ['directeur', 'secretaire', 'censeur']:
        return HttpResponseForbidden("Aksè refize.")
    
    error = verify_active_session(request)
    if error:
        return error

    # 🔍 Récupérer le terme de recherche
    search_query = request.GET.get('search', '').strip()

    # 🔍 Filtrer les élèves
    eleves = Eleve.objects.all()
    if search_query:
        eleves = eleves.filter(
            Q(code_eleve__icontains=search_query) |
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(classe__icontains=search_query)
        )

    context = {
        'eleves': eleves,
        'role': role,
        'search_query': search_query,  # Pour pré-remplir le champ
    }
    return render(request, 'app_eleve/eleve.html', context)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
def toggle_actif_eleve(request, id):
    try:
        eleve = Eleve.objects.get(id=id)
        data = json.loads(request.body)
        eleve.actif = data.get('actif', True)
        eleve.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    





# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def eleve_details(request, id):
    eleve = get_object_or_404(Eleve, id=id)
    data = {
        "id": eleve.id,
        "code_eleve": eleve.code_eleve,
        "nom": eleve.nom,
        "prenom": eleve.prenom,
        "sexe": eleve.sexe,
        "adresse": eleve.adresse,
        "classe": eleve.classe,
        "telephone": eleve.telephone,
        "nom_tuteur": eleve.nom_tuteur,
        "telephone_tuteur": eleve.telephone_tuteur,
        "email": eleve.email,
        "date_naissance": eleve.date_naissance.strftime("%d/%m/%Y") if eleve.date_naissance else None,
        "date_naissance_raw": eleve.date_naissance.strftime("%Y-%m-%d") if eleve.date_naissance else "",
        "annee_academique": eleve.annee_academique,
        "lieu_naissance": eleve.lieu_naissance,
        "actif": eleve.actif,
        "photo_url": eleve.photo.url if eleve.photo else None,
    }
    return JsonResponse(data)






from datetime import datetime, date  # si tu as besoin des deux
@require_http_methods(["POST"])
def modifier_eleve(request, id):
    try:
        eleve = get_object_or_404(Eleve, id=id)

        eleve.nom = request.POST.get("nom", "").strip()
        eleve.prenom = request.POST.get("prenom", "").strip()
        eleve.sexe = request.POST.get("sexe", "").strip()
        eleve.adresse = request.POST.get("adresse", "").strip()
        eleve.classe = request.POST.get("classe", "").strip()
        eleve.telephone = request.POST.get("telephone", "").strip()
        eleve.email = request.POST.get("email", "").strip().lower()
        eleve.nom_tuteur = request.POST.get("nom_tuteur", "").strip()
        eleve.telephone_tuteur = request.POST.get("telephone_tuteur", "").strip() 

        # Date de naissance
        date_naiss = request.POST.get("date_naissance")
        if date_naiss:
            try:
                eleve.date_naissance = datetime.strptime(date_naiss, "%Y-%m-%d").date()
            except:
                pass

        eleve.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)





from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_eleve.models import Eleve  # Asire model Eleve a egziste

@api_view(['GET'])
def total_eleves(request):
    total = Eleve.objects.count()
    return Response({"total": total})
