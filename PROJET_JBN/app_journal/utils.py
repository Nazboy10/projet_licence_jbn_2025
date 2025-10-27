# app_journal/utils.py
from .models import AuditLog

def log_action(request, action, objet_type, objet_id, description=""):
    """
    Fonksyon pou senplifye tracabilite.
    request: HttpRequest (pou jwenn itilizatè, ip)
    action: 'ajoute', 'modifye', 'efase', elatriye
    objet_type: 'Inscription', 'Utilisateur', elatriye
    objet_id: ID obje ki afekte
    description: deskripsyon aksyon an (si nesesè)
    """
    AuditLog.objects.create(
        action=action,
        objet_type=objet_type,
        objet_id=objet_id,
        utilisateur_id=request.session.get('id'),
        utilisateur_role=request.session.get('role'),
        utilisateur_username=request.session.get('username'),
        ip_address=request.META.get('REMOTE_ADDR'),
        description=description
    )