# api/serializers.py
from rest_framework import serializers
from SGCBA.models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'role']  # Nou pa ekspoze modpas
