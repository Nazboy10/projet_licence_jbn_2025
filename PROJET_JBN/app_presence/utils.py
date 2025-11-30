# app_presence/utils.py
from django.utils import timezone
from app_eleve.models import Eleve
from app_inscription.models import Inscription
from .models import Presence
from app_classe.models import Classe

def assurer_presences_jour(date=None):
    """
    Pour chaque élève actif, s'assure qu'une entrée Presence existe pour `date`.
    Si non, crée une entrée avec statut='absent'.
    """
    if date is None:
        date = timezone.now().date()

    # Récupérer tous les élèves actifs
    eleves_actifs = Eleve.objects.filter(actif=True)

    for eleve in eleves_actifs:
        # Trouver l'inscription correspondante (même code_eleve)
        try:
            inscription = Inscription.objects.get(code_eleve=eleve.code_eleve)
        except Inscription.DoesNotExist:
            continue  # ou log erreur

        # Vérifier si présence existe déjà
        if not Presence.objects.filter(eleve=inscription, date=date).exists():
            # Déterminer la classe (à partir de Inscription ou Eleve)
            klas_obj = None
            if inscription.classe:
                klas_obj = Classe.objects.filter(
                    nom_classe__iexact=inscription.classe.strip()
                ).first()

            # Créer l'absence
            Presence.objects.create(
                eleve=inscription,
                date=date,
                klas=klas_obj,
                statut='absent'
            )