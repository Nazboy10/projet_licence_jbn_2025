from django.db import models
from django.contrib.auth.hashers import make_password, check_password

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

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Create your models here.
