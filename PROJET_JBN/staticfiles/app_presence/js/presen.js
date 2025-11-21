// app_presence/js/Presence.js
document.addEventListener('DOMContentLoaded', () => {
    // ... (kòd ki deja la pou dropdown, QR, elatriye) ...
    const toggle = document.getElementById('profileDropdownToggle');
    const dropdown = document.getElementById('profileDropdown');

    if (toggle && dropdown) {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation(); // Pa fè click la monte nan document
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', () => {
            dropdown.style.display = 'none';
        });

           // Confirmation de déconnexion (remplacé par SweetAlert2)
        const logoutLink = dropdown.querySelector("a");
        if (logoutLink) {
            logoutLink.addEventListener('click', function(e) {
                e.preventDefault();
                Swal.fire({
                  title: 'Déconnexion',
                  text: "Êtes-vous sûr de vouloir déconnecter ?",
                  icon: 'warning',
                  showCancelButton: true,
                  confirmButtonText: 'Oui',
                  cancelButtonText: 'Non'
                }).then((result) => {
                  if (result.isConfirmed) {
                    window.location.href = this.href;
                  }
                });
            });
        }
    }



    // Elements pou presans
    const btnShowForm = document.getElementById('btnShowForm');
    const formModal = document.getElementById('formModal');
    const closeModal = document.getElementById('closeModal');
    const cancelForm = document.getElementById('cancelForm');
    const presenceForm = document.getElementById('presenceForm');
    const codeInput = document.getElementById('code_eleve');
    const nomInput = document.getElementById('nom_eleve');
    const prenomInput = document.getElementById('prenom_eleve');
    const classeInput = document.getElementById('classe_eleve');
    const dateInput = document.getElementById('date_presence');

    // Mete dat jodi a kòm default
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;

    // Afficher modal
    btnShowForm.addEventListener('click', () => {
        resetForm();
        formModal.style.display = 'flex';
    });

    // Fermer modal
    [closeModal, cancelForm].forEach(btn => {
        btn.addEventListener('click', () => {
            formModal.style.display = 'none';
            resetForm();
        });
    });

    // Kòd pou chache elèv
    codeInput.addEventListener('input', async () => {
        const code = codeInput.value.trim();
        if (code.length > 0) {
            try {
                const response = await fetch(`/presence/get_eleve_by_code/?code=${encodeURIComponent(code)}`);
                const data = await response.json();

                if (data.success) {
                    nomInput.value = data.nom;
                    prenomInput.value = data.prenom;
                    classeInput.value = data.classe;
                } else {
                    nomInput.value = '';
                    prenomInput.value = '';
                    classeInput.value = '';
                    if (data.error) {
                        console.error(data.error);
                        // Ou kapab mete yon mesaj erè sou HTML la tou
                    }
                }
            } catch (error) {
                console.error('Erè lè chache elèv:', error);
                nomInput.value = '';
                prenomInput.value = '';
                classeInput.value = '';
            }
        } else {
            // Si code vide, vide tout chan
            resetForm();
        }
    });

    // Submit form presans
   presenceForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(presenceForm);
    const code = formData.get('code_eleve').trim();
    const date = formData.get('date_presence');
    const statut = 'present';

    if (!code) {
        alert('Mete code elèv la.');
        return;
    }

    try {
        const response = await fetch('/presence/', {
            method: 'POST',
            body: new URLSearchParams({
                'code_eleve': code,
                'date': date,
                'statut': statut,
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json(); // ✅ Li JSON la

        if (response.ok) {
            Swal.fire("Succès !", data.message, "success");
            formModal.style.display = 'none';
            resetForm();
            setTimeout(() => location.reload(), 800);
        } else {
            // ✅ Jere doublon kòrèk
            Swal.fire("Avertissement", data.error || "Erè!", "warning");
        }

    } catch (error) {
        console.error(error);
        Swal.fire("Erreur", "Erè kote kliyan.", "error");
    }


    
});

  // 🎯 Recherche filtre presence nan tab
const searchInput = document.getElementById("searchPresence");
const table = document.getElementById("tableEleves").getElementsByTagName("tbody")[0];

if (searchInput) {
    searchInput.addEventListener("keyup", function () {
        const query = this.value.toLowerCase().trim();

        const rows = table.getElementsByTagName("tr");

        for (let row of rows) {
            const cells = row.getElementsByTagName("td");
            let found = false;

            // Parcours chaque cellule pour voir si la requête correspond
            for (let cell of cells) {
                if (cell.innerText.toLowerCase().includes(query)) {
                    found = true;
                    break;
                }
            }

            // Affiche ou masque la ligne
            row.style.display = found ? "" : "none";
        }
    });
}

    function resetForm() {
        codeInput.value = '';
        nomInput.value = '';
        prenomInput.value = '';
        classeInput.value = '';
        dateInput.value = today; // Mete jodi a ankò
    }

   // === GESTION DES NOTIFICATIONS ===

const bellIcon = document.getElementById('notificationBell');
const notificationBadge = document.getElementById('notificationBadge');
const notificationDropdown = document.getElementById('notificationDropdown');
const notificationList = document.getElementById('notificationList');

// Fonction pour charger les notifications non lues
async function chargerNotifications() {
    try {
        const res = await fetch('/presence/notifications/non-lues/', {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();
        const count = data.nombre_non_lus;

        if (count > 0) {
            notificationBadge.textContent = count;
            notificationBadge.style.display = 'block';
        } else {
            notificationBadge.style.display = 'none';
        }
    } catch (err) {
        console.error('Erreur chargement notifications:', err);
    }
}

// Fonction pour charger les dernières notifications et les marquer comme lues
async function chargerDernieresNotifications() {
    try {
        const res = await fetch('/presence/notifications/dernieres/', {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();

        notificationList.innerHTML = '';

        if (data.notifications.length === 0) {
            Swal.fire({
                icon: 'info',
                title: 'Aucune notification',
                text: 'Aucune présence récente.',
                timer: 2000,
                showConfirmButton: false
            });
        } else {
            // ✅ Construire le message à afficher
            let message = '<div style="text-align: left;">';
            data.notifications.forEach(n => {
                message += `
                    <div class="notification-item">
                      <strong>${n.nom} ${n.prenom}</strong>
                      <small class="text-muted">(${n.classe}) - ${n.date_scan}</small>
                      <hr style="margin:5px 0;">
                    </div>
                `;
            });
            message += '</div>';

            // ✅ Affiche une popup avec SweetAlert2
            Swal.fire({
                title: 'Notifications de Présence',
                html: message,
                icon: 'info',
                confirmButtonText: 'Fermer',
                width: '400px'
            });
        }

        // ✅ Marquer toutes les notifications comme lues
        await fetch('/presence/mark-notifications-read/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        // ✅ Mettre à jour le badge à 0 IMMÉDIATEMENT dans l'interface
        const notificationBadge = document.getElementById('notificationBadge');
        if (notificationBadge) {
            notificationBadge.style.display = 'none';
        }

    } catch (err) {
        console.error('Erreur chargement liste notifications:', err);
    }
}

// Charger les notifications au démarrage
chargerNotifications();

// Rafraîchir toutes les 30 secondes
setInterval(chargerNotifications, 30000);

// Ouvrir le dropdown des notifications
if (bellIcon) {
    bellIcon.addEventListener('click', async (e) => {
        e.stopPropagation();
        notificationDropdown.style.display = notificationDropdown.style.display === 'block' ? 'none' : 'block';

        if (notificationDropdown.style.display === 'block') {
            await chargerDernieresNotifications();
        }
    });
}

// Fermer le dropdown si on clique ailleurs
document.addEventListener('click', () => {
    notificationDropdown.style.display = 'none';
});

});