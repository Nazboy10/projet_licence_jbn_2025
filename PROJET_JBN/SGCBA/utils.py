# SGCBA/utils.py
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Utilisateur

def verify_active_session(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('connexion')
    
    try:
        user = Utilisateur.objects.get(id=user_id)
        if user.session_key != request.session.session_key:
            logout(request)
            return redirect('connexion')
    except Utilisateur.DoesNotExist:
        return redirect('connexion')
    
    return None  # Session valide