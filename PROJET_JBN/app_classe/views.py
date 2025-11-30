from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q  # ← Ajout nécessaire pour la recherche
from .models import Classe
from app_parametre.models import Parametre
from app_journal.utils import log_action 
from SGCBA.utils import verify_active_session
# views.py
def classe(request):
    error = verify_active_session(request)
    if error:
        return error

    role = request.session.get('role', None)

    # 🔍 Recherche + pagination (inchangé)
    search_query = request.GET.get('search', '').strip()
    classes_list = Classe.objects.all()
    if search_query:
        classes_list = classes_list.filter(
            Q(nom_classe__icontains=search_query) |
            Q(code_classe__icontains=search_query) |
            Q(niveau__icontains=search_query) |
            Q(annee_academique__icontains=search_query)
        )

    classes_list = classes_list.order_by('-id')
    paginator = Paginator(classes_list, 5)
    page_number = request.GET.get('page')
    try:
        classes = paginator.page(page_number)
    except PageNotAnInteger:
        classes = paginator.page(1)
    except EmptyPage:
        classes = paginator.page(paginator.num_pages)

    param = Parametre.load()
    context = {
        'classes': classes,
        'annee_academique': param.annee_academique,
        'search_query': search_query,
        'role': role,
    }
    return render(request, "app_classe/classe.html", context)





# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@require_http_methods(["POST"])
def ajouter_classe_api(request):
    nom = request.POST.get("nom_classe", "").strip()
    niveau = request.POST.get("niveau", "").strip()
    annee_academique = request.POST.get("annee_academique", "").strip()

    if not nom or not niveau:
        return JsonResponse({"success": False, "error": "Tous les champs sont requis."}, status=400)

    if Classe.objects.filter(nom_classe__iexact=nom).exists():
        return JsonResponse({"success": False, "error": f"Une classe nommée « {nom} » existe déjà."}, status=400)

    klas = Classe.objects.create(
        nom_classe=nom,
        niveau=niveau,
        annee_academique=annee_academique
    )

    log_action(
        request=request,
        action='ajoute',
        objet_type='Classe',
        objet_id=klas.id,
        description=f"Klas ID {klas.id} ({klas.nom_classe}) te ajoute pa {request.session.get('username')}."
    )

    return JsonResponse({"success": True, "message": "Classe ajoutée avec succès !"})









# modification
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Classe

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Classe

def modifier_classe(request, id):
    classe = get_object_or_404(Classe, id=id)
    
    if request.method == "POST":
        nom = request.POST.get("nom_classe", "").strip()
        niveau = request.POST.get("niveau", "").strip()
        
        if not nom or not niveau:
            messages.error(request, "Veuillez remplir tous les champs requis.")
        elif Classe.objects.filter(nom_classe__iexact=nom).exclude(id=id).exists():
            messages.error(request, f"Une classe nommée « {nom} » existe déjà.")
        else:
            old_nom = classe.nom_classe
            old_niveau = classe.niveau
            classe.nom_classe = nom
            classe.niveau = niveau
            classe.save()

             # ✅ Kenbe aksyon an
            log_action(
                request=request,
                action='modifye',
                objet_type='Classe',
                objet_id=classe.id,
                description=f"Klas ID {classe.id} te modifye pa {request.session.get('username')}. Avan: {old_nom} ({old_niveau}), Kounye: {classe.nom_classe} ({classe.niveau})."
            )

            messages.success(request, "La classe a été modifiée avec succès !")
        
        return redirect('classe')
    
    # En GET : renvoyer JSON pour le modal
    return JsonResponse({
        "id": classe.id,
        "nom_classe": classe.nom_classe,
        "niveau": classe.niveau,
        "annee_academique": classe.annee_academique
    })


#  LA FONCTION DE SUPPRESSION 
from django.http import JsonResponse

def supprimer_classe(request, id):
    if request.method == "POST":
        try:
            classe = Classe.objects.get(id=id)
              # ✅ Kenbe aksyon an avan efase
            log_action(
                request=request,
                action='efase',
                objet_type='Classe',
                objet_id=classe.id,
                description=f"Klas ID {classe.id} ({classe.nom_classe}) te efase pa {request.session.get('username')}."
            )
            classe.delete()
            return JsonResponse({"success": True})
        except Classe.DoesNotExist:
            return JsonResponse({"success": False, "error": "Classe introuvable."})
        
        
    return JsonResponse({"success": False, "error": "Requête invalide."})




# app_classe/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from app_eleve.models import Eleve  # ✅ Importer Eleve au lieu de Inscription
from .models import Classe

def get_eleves_par_classe(request, classe_id):
    """
    Renvoie la liste des élèves ACTIFS d'une classe donnée (à partir du modèle Eleve).
    """
    try:
        classe = get_object_or_404(Classe, id=classe_id)
        # ✅ Filtrer les élèves actifs dont le champ 'classe' correspond à 'nom_classe' de la classe
        eleves = Eleve.objects.filter(
            classe=classe.nom_classe,  # Correspondance : Eleve.classe == Classe.nom_classe
            actif=True                 # Seulement les élèves actifs
        ).values(
            'code_eleve', 'nom', 'prenom', 'sexe', 'telephone'
        )
        return JsonResponse({
            'success': True,
            'classe_nom': classe.nom_classe,
            'eleves': list(eleves)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)