from rest_framework import permissions

class IsDirecteur(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.session.get('role')
        return role == 'directeur'
