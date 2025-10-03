# api/serializers.py
from rest_framework import serializers
from SGCBA.models import Utilisateur
import re


class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'role', 'nom', 'prenom', 'password', 'actif', 'photo']

    def validate(self, attrs):
        """
        Validation générale : s'assurer qu'un mot de passe est fourni à la création
        et qu'il respecte les règles définies.
        """
        # Si création (pas d'instance) -> password requis
        if not getattr(self, 'instance', None) and 'password' not in attrs:
            raise serializers.ValidationError({'password': "Mot de passe requis à la création."})

        # Si un mot de passe est fourni (création ou update), valider sa complexité
        pwd = attrs.get('password')
        if pwd is not None:
            errors = []
            if len(pwd) < 8:
                errors.append("Au moins 8 caractères")
            if not re.search(r'[A-Z]', pwd):
                errors.append("Au moins une lettre majuscule")
            if not re.search(r'\d', pwd):
                errors.append("Au moins un chiffre")
            if not re.search(r'[!@#$%^&*()_\-+=<>?]', pwd):
                errors.append("Au moins un caractère spécial (!@#$%^&*()_-+=<>?)")

            if errors:
                raise serializers.ValidationError({'password': ' ; '.join(errors)})

        return attrs

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
        # Lors d'une update, autoriser la même adresse si elle appartient à l'instance
        qs = Utilisateur.objects.filter(email=value)
        if getattr(self, 'instance', None):
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Cet email existe déjà.")
        return value

    def validate_username(self, value):
        qs = Utilisateur.objects.filter(username=value)
        if getattr(self, 'instance', None):
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ce nom d’utilisateur existe déjà.")
        return value
