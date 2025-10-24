from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q  # ← Ajout nécessaire pour la recherche
from .models import Classe
from app_parametre.models import Parametre

def classe(request):
    if request.method == "POST":
        nom = request.POST.get("nom_classe", "").strip()
        niveau = request.POST.get("niveau", "").strip()
        
        if not nom or not niveau:
            messages.error(request, "Veuillez remplir tous les champs requis.")
        elif Classe.objects.filter(nom_classe__iexact=nom).exists():
            messages.error(request, f"Une classe nommée « {nom} » existe déjà.")
        else:
            Classe.objects.create(nom_classe=nom, niveau=niveau)
            messages.success(request, "La classe a été ajoutée avec succès !")
        
        # Conserver le terme de recherche après soumission
        search_query = request.GET.get('search', '')
        if search_query:
            return redirect(f"{request.path}?search={search_query}")
        return redirect('classe')

    # 🔍 Récupérer le terme de recherche depuis l'URL (?search=...)
    search_query = request.GET.get('search', '').strip()

    # 🔍 Filtrer les classes si un terme est fourni
    classes_list = Classe.objects.all()
    if search_query:
        classes_list = classes_list.filter(
            Q(nom_classe__icontains=search_query) |
            Q(code_classe__icontains=search_query) |
            Q(niveau__icontains=search_query) |
            Q(annee_academique__icontains=search_query)
        )

    classes_list = classes_list.order_by('-id')

    # 📄 Pagination : 5 éléments par page
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
        'search_query': search_query,  # ← pour pré-remplir le champ de recherche
    }
    return render(request, "app_classe/classe.html", context)

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
            classe.nom_classe = nom
            classe.niveau = niveau
            classe.save()
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
            classe.delete()
            return JsonResponse({"success": True})
        except Classe.DoesNotExist:
            return JsonResponse({"success": False, "error": "Classe introuvable."})
    return JsonResponse({"success": False, "error": "Requête invalide."})
