# SGCBA/middleware.py
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Utilisateur

class TokenSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs exemptées (utilisez des chemins fixes pour éviter les erreurs de reverse)
        exempt_paths = [
            '/connexion/',
            '/logout/',
            '/reset_password',
            '/static/',
            '/media/',
            '/api/',  # APIs gèrent leur propre auth
        ]

        # Ne pas appliquer aux URLs exemptées
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)

        # Vérifier la session
        user_id = request.session.get('id')
        session_token = request.session.get('token')

        if user_id and session_token:
            try:
                user = Utilisateur.objects.get(id=user_id)
                if user.token != session_token:
                    logout(request)
                    return redirect('/connexion/')
            except Utilisateur.DoesNotExist:
                pass

        return self.get_response(request)