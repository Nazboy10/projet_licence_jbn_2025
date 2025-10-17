# app_parametre/models.py
from django.db import models

class Parametre(models.Model):
    # Généraux
    nom_etablissement = models.CharField(max_length=200, default="Collège Belle Angelot")
    annee_academique = models.CharField(max_length=20, default="2025-2026")
    trimestre = models.IntegerField(default=1)  # 1, 2, ou 3
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to='parametres/', null=True, blank=True)

    # Académiques
    regle_passage = models.BooleanField(default=False)

    # Utilisateurs
    session_duration = models.IntegerField(default=120)  # minutes
    pw_reset = models.BooleanField(default=True)

    # Communication
    email_contact = models.EmailField(blank=True)
    tel_contact = models.CharField(max_length=20, blank=True)

    # Sécurité
    backup_auto = models.BooleanField(default=True)
    logs_active = models.BooleanField(default=True)

    # Singleton
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Paramètres du système"