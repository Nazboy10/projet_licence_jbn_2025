# app_eleve/models.py
from django.db import models

class Eleve(models.Model):
    code_eleve = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10)
    adresse = models.CharField(max_length=200)
    classe = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    nom_tuteur = models.CharField(max_length=100)
    telephone_tuteur = models.CharField(max_length=20)
    annee_academique = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField(null=True, blank=True)  # Car peut-être vide
    email = models.EmailField(blank=True, null=True)

    # ✅ nouvo chan yo
    photo = models.ImageField(upload_to='eleves_photos/', blank=True, null=True)
    actif = models.BooleanField(default=True)

    date_enregistrement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.code_eleve}"
