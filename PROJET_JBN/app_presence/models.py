# app_presence/models.py
from django.db import models
from app_inscription.models import Inscription  # Elèv yo sòti nan app_inscription
from app_classe.models import Classe  # Si w vle mete klas la tou
from django.utils import timezone
import secrets 

class Presence(models.Model):
    STATUT_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('justifier', 'Justifier'),  # Si nesesè
    ]

    eleve = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='presences')
    date = models.DateField(default=timezone.now)  # Jounen presans lan
    klas = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True)  # Opsyonel
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='present')
    # Si w vle: matyè, oswa lè (pou chak leson), elatriye

    def __str__(self):
        return f"{self.eleve.nom} {self.eleve.prenom} - {self.date} - {self.statut}"

    class Meta:
        unique_together = ('eleve', 'date', 'klas')  # Yon elèv pa kapab gen 2 presans pou menm jounen/klas
        db_table = "app_presence"








class QRPermanent(models.Model):
    classe = models.OneToOneField(Classe, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True, default=secrets.token_urlsafe(16))

    def __str__(self):
        return f"QR pour {self.classe.nom_classe}"

    class Meta:
        db_table = "app_presence_qr_permanent"







# app_presence/models.py
from django.db import models
from app_inscription.models import Inscription
from app_classe.models import Classe
from django.utils import timezone

class NotificationScan(models.Model):
    eleve = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    date_scan = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)  # Pour savoir si l'admin a vu la notification

    def __str__(self):
        return f"{self.eleve.nom} {self.eleve.prenom} - {self.date_scan.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        db_table = "app_presence_notification_scan"
        ordering = ['-date_scan']  # Les plus récents en premier