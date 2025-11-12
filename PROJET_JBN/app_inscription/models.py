from django.db import models

class Inscription(models.Model):
    code_eleve = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10)
    adresse = models.CharField(max_length=255)
    annee_academique = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField()
    classe = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    nom_tuteur = models.CharField(max_length=100)
    tel_tuteur = models.CharField(max_length=15)
    date_inscription = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    class Meta:
        db_table = "app_inscription_eleve"  # 👈 sa chanje non tab la sèlman
