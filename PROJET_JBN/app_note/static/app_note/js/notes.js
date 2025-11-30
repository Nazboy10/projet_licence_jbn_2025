document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('profileDropdownToggle');
    const dropdown = document.getElementById('profileDropdown');

    if (toggle && dropdown) {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation(); // Pa fè click la monte nan document
            // Toggle display
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });

        // Fèmen dropdown lè w klike nenpòt lòt kote
        document.addEventListener('click', () => {
            dropdown.style.display = 'none';
        });

        // Pa fè dropdown la fèmen si w klike andedan li
        dropdown.addEventListener('click', (e) => {
            e.stopPropagation();
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

    // === Modal gestion notes ===
    const btnShowForm = document.getElementById('btnShowForm');
    const formModal = document.getElementById('formModal');
    const closeModal = document.getElementById('closeModal');
    const cancelForm = document.getElementById('cancelForm');
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const inputCodeEleve = document.getElementById('inputCodeEleve');
    const btnVerifyCode = document.getElementById('btnVerifyCode');
    const codeError = document.getElementById('codeError');
    const nomEleve = document.getElementById('nomEleve');
    const prenomEleve = document.getElementById('prenomEleve');
    const classeEleve = document.getElementById('classeEleve');
    const notesFields = document.getElementById('notesFields');
    const addNoteRow = document.getElementById('addNoteRow');
    const successMessage = document.getElementById('successMessage');

    let currentCodeEleve = null;

    // Charger les matières depuis l’API
    let matieresList = [];
    fetch('/note/api/matieres/')
        .then(res => res.json())
        .then(data => {
            matieresList = data;
        });

    function createNoteRow(matiereId = '', noteValue = '') {
        const div = document.createElement('div');
        div.classList.add('row', 'g-2', 'mb-2', 'noteRow');
        const options = matieresList.map(m =>
            `<option value="${m.id}" ${m.id == matiereId ? 'selected' : ''}>${m.nom}</option>`
        ).join('');
        div.innerHTML = `
            <div class="col">
                <select class="form-select" required>
                    <option value="">Choisir matière</option>
                    ${options}
                </select>
            </div>
            <div class="col">
                <input type="number" class="form-control" step="0.01" min="0" max="100" value="${noteValue}" placeholder="Note" required>
            </div>
            <div class="col-auto d-flex align-items-end">
                <button type="button" class="btn btn-outline-danger btn-sm remove-row">✕</button>
            </div>
        `;
        notesFields.appendChild(div);

        // Suppression ligne
        div.querySelector('.remove-row').addEventListener('click', () => div.remove());
    }

    btnShowForm.addEventListener('click', () => {
        formModal.style.display = 'flex';
        step1.style.display = 'block';
        step2.style.display = 'none';
        codeError.style.display = 'none';
        inputCodeEleve.value = '';
        successMessage.style.display = 'none';
        notesFields.innerHTML = '';
        createNoteRow();
        createNoteRow();
    });

    [closeModal, cancelForm].forEach(btn => {
        btn.addEventListener('click', () => formModal.style.display = 'none');
    });

    btnVerifyCode.addEventListener('click', async () => {
        const code = inputCodeEleve.value.trim();
        if (!code) {
            codeError.style.display = 'block';
            codeError.textContent = 'Veuillez entrer un code.';
            return;
        }

        try {
            const res = await fetch('/note/api/verifier-eleve/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')  // ⚠️ important
                },
                body: `code=${encodeURIComponent(code)}`
            });
            const data = await res.json();

            if (data.existe) {
                codeError.style.display = 'none';
                step1.style.display = 'none';
                step2.style.display = 'block';
                nomEleve.textContent = data.nom;
                prenomEleve.textContent = data.prenom;
                classeEleve.textContent = data.classe;
                currentCodeEleve = code;
            } else {
                codeError.style.display = 'block';
                codeError.textContent = 'Élève non trouvé ou non validé.';
                step2.style.display = 'none';
            }
        } catch (e) {
            alert('Erreur de connexion au serveur.');
        }
    });

    addNoteRow.addEventListener('click', () => createNoteRow());

    // Soumission des notes
    const formNotes = document.getElementById('formNotes');
    if (formNotes) {
        formNotes.addEventListener('submit', async (e) => {
            e.preventDefault();
            const rows = notesFields.querySelectorAll('.noteRow');
            const notes = [];

            for (const row of rows) {
                const select = row.querySelector('select');
                const input = row.querySelector('input');
                if (!select.value || !input.value) continue;
                notes.push({
                    matiere_id: select.value,
                    valeur: parseFloat(input.value)
                });
            }

            if (notes.length === 0) {
                alert('Veuillez entrer au moins une note.');
                return;
            }

            try {
                const response = await fetch('/note/api/enregistrer-notes/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        code_eleve: currentCodeEleve,
                        notes: notes
                    })
                });

                const result = await response.json();
                if (response.ok) {
                    successMessage.style.display = 'block';
                    setTimeout(() => formModal.style.display = 'none', 2000);
                     chargerNotes();
                } else {
                    alert('Erreur : ' + (result.erreur || 'Échec'));
                }
            } catch (e) {
                alert('Erreur réseau : ' + e.message);
            }
        });
    }



     // Charger et afficher les notes
function chargerNotes() {
    const tbody = document.getElementById('tableElevesBody');
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">Chargement...</td></tr>';

    fetch('/note/api/notes/')
        .then(res => res.json())
        .then(eleves => {
            if (eleves.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center">Aucune note enregistrée.</td></tr>';
                return;
            }

            tbody.innerHTML = '';
            eleves.forEach(el => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${el.code_eleve}</td>
                    <td>${el.nom}</td>
                    <td>${el.prenom}</td>
                    <td>${el.classe}</td>
                   
                    
                    <td>
                        <button class="btn btn-sm btn-outline-info show-notes" data-notes='${JSON.stringify(el.matieres_notes)}'>
                            👁️ Voir notes
                        </button>
                    </td>
                    <td>
                        <button class="btn btn-warning btn-sm edit-note" data-code="${el.code_eleve}">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-danger btn-sm delete-note" data-code="${el.code_eleve}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });

            // Ajouter l'écouteur pour le bouton "Voir notes"
            document.querySelectorAll('.show-notes').forEach(btn => {
                btn.addEventListener('click', function() {
                    const notes = JSON.parse(this.dataset.notes);
                    const modal = document.getElementById('notesModal');
                    const list = document.getElementById('modalNotesList');
                    const nomSpan = document.getElementById('modalEleveNom');

                    // Afficher le nom de l'élève (tu peux aussi stocker nom/prénom dans data)
                    const row = this.closest('tr');
                    const nom = row.children[1].textContent;
                    const prenom = row.children[2].textContent;
                    nomSpan.textContent = `${prenom} ${nom}`;

                    // Remplir la liste
                    list.innerHTML = '';
                    notes.forEach(n => {
                        const li = document.createElement('li');
                        li.innerHTML = `<strong>${n.matiere}:</strong> ${n.valeur}`;
                        list.appendChild(li);
                    });

                    modal.style.display = 'block';
                });
            });

            // Fermer le modal
            document.getElementById('closeNotesModal').addEventListener('click', () => {
                document.getElementById('notesModal').style.display = 'none';
            });
        })
        .catch(err => {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Erreur de chargement.</td></tr>';
            console.error("Erreur :", err);
        });
}








// Appelle au chargement de la page
chargerNotes();










});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}