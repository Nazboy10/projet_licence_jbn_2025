# app_journal/views.py
from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import AuditLog
from django.core.paginator import Paginator

def journal_activite(request):
    if request.session.get('role') != 'directeur':
        return HttpResponseForbidden("Aksè refize.")
    
    logs = AuditLog.objects.all()

     # Pajinasyon
    paginator = Paginator(logs, 10)  # 10 liy pa paj
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    return render(request, 'app_journal/journal.html', {'logs': page_obj})  # ✅ Ou dwe itilize "page_obj"