# app_classe/models.py
from django.db import models
from app_parametre.models import Parametre  # pou pran annee akadémik la

class Classe(models.Model):
    code_classe = models.CharField(max_length=20, unique=True, editable=False)
    nom_classe = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)
    annee_academique = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.pk:  # Sèlman lè li nouvo
            param = Parametre.load()
            annee_courte = param.annee_academique.split('-')[0]  # "2025-2026" → "2025"
            
            # Pran dènye nimewo pou ane sa a
            dernier = Classe.objects.filter(
                annee_academique=param.annee_academique
            ).order_by('code_classe').last()

            if dernier:
                # Ektrè nimewo sòti kòd la (ex: CLS-2025-042 → 42)
                dernier_num = int(dernier.code_classe.split('-')[-1])
                nouveau_num = dernier_num + 1
            else:
                nouveau_num = 1

            self.annee_academique = param.annee_academique
            self.code_classe = f"CLS-{annee_courte}-{nouveau_num:03d}"  # ex: CLS-2025-001

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code_classe} - {self.nom_classe} ({self.niveau})"