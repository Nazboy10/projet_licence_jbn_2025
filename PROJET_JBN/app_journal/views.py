# app_journal/views.py
from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import AuditLog

def journal_activite(request):
    if request.session.get('role') != 'directeur':
        return HttpResponseForbidden("Aksè refize.")

    logs = AuditLog.objects.all()
    return render(request, 'app_journal/journal.html', {'logs': logs})