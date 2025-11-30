# app_note/models.py

from django.db import models
from app_eleve.models import Eleve
from SGCBA.models import Utilisateur  # Ton modèle utilisateur personnalisé

class Matiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class Note(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    valeur = models.DecimalField(max_digits=5, decimal_places=2)
    date_saisie = models.DateTimeField(auto_now_add=True)
    periode = models.CharField(
        max_length=20,
        choices=[
            ('1er_trimestre', '1er Trimestre'),
            ('2eme_trimestre', '2ème Trimestre'),
            ('3eme_trimestre', '3ème Trimestre'),
        ],
        default='1er_trimestre'
    )
    annee_academique = models.CharField(max_length=20, default="2025-2026")
    saisi_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('eleve', 'matiere')

    def __str__(self):
        return f"{self.eleve} - {self.matiere}: {self.valeur}"