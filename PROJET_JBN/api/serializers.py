# api/serializers.py
from rest_framework import serializers
from SGCBA.models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'role', 'nom', 'prenom', 'password', 'actif', 'photo']

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        nom = validated_data.pop('nom', '')
        prenom = validated_data.pop('prenom', '')
        actif = validated_data.pop('actif', True)

        user = Utilisateur(**validated_data)
        user.nom = nom
        user.prenom = prenom
        user.actif = actif
        user.set_password(raw_password)
        user.save()
        return user

    def update(self, instance, validated_data):  # ✅ kounya anndan klas la
        raw_password = validated_data.pop('password', None)
        if raw_password:
            instance.set_password(raw_password)

        # update lòt chan yo
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate_email(self, value):
        if Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email existe déjà.")
        return value

    def validate_username(self, value):
        if Utilisateur.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d’utilisateur existe déjà.")
        return value
