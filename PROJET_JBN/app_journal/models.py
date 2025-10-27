# app_journal/models.py
from django.db import models
from django.utils import timezone

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('ajoute', 'Ajoute'),
        ('modifye', 'Modifye'),
        ('efase', 'Efase'),
        ('konekte', 'Konekte'),
        ('dekonekte', 'Dekonekte'),
        ('valide', 'Valide'),
        ('desaktive', 'Desaktive'),
        ('telechaje', 'Telechaje'),
        # Ajoute lòt aksyon selon nesesite
    ]

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    objet_type = models.CharField(max_length=50)  # ex: "Inscription", "Utilisateur", "Eleve", "Note"
    objet_id = models.IntegerField(null=True, blank=True)  # ID obje ki afekte (ex: ID enskripsyon)
    description = models.TextField(blank=True)  # Deskripsyon aksyon an (si nesesè)
    utilisateur_id = models.IntegerField()  # ID itilizatè ki fè aksyon an
    utilisateur_role = models.CharField(max_length=20)  # ex: 'directeur'
    utilisateur_username = models.CharField(max_length=150)  # ex: 'admin123'
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # IP itilizatè a (opsyonèl)
    date_action = models.DateTimeField(default=timezone.now)  # Dat epi lè aksyon an

    def __str__(self):
        return f"[{self.date_action}] {self.utilisateur_username} ({self.utilisateur_role}) - {self.action} sou {self.objet_type} ID {self.objet_id}"

    class Meta:
        db_table = "app_journal_log"
        ordering = ['-date_action']  # Triye aksyon yo pa dat (pi resan an premye)