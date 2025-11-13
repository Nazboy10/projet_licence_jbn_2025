# app_bulletin/models.py
from django.db import models
from app_eleve.models import Eleve
from SGCBA.models import Utilisateur 



class Bulletin(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    periode = models.CharField(
        max_length=20,
        choices=[
            ('1er_trimestre', '1er Trimestre'),
            ('2eme_trimestre', '2ème Trimestre'),
            ('3eme_trimestre', '3ème Trimestre'),
        ],
        default='1er_trimestre'
    )
    moyenne = models.DecimalField(max_digits=5, decimal_places=2)
    mention = models.CharField(max_length=20)
    date_generation = models.DateTimeField(auto_now_add=True)
    genere_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Bulletin {self.periode} - {self.eleve}"