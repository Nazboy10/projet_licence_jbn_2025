from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import secrets

class Utilisateur(models.Model):
    ROLE_CHOICES = (
        ('directeur', 'Directeur'),
        ('secretaire', 'Secretaire'),
        ('censeur', 'Censeur'),
    )

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=20,)
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    actif = models.BooleanField(default=True) 
    photo = models.ImageField(upload_to="photos_profil/", default="photos_profil/pro.png", blank=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def generate_token(self):
        self.token = secrets.token_hex(20)
        self.save()
        return self.token

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} {self.nom} {self.prenom} ({self.role})"

# Create your models here.
