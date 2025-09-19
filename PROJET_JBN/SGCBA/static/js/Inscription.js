document.addEventListener('DOMContentLoaded', () => {
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

        // Confirmation de déconnexion
        const logoutLink = dropdown.querySelector("a");
        if (logoutLink) {
            logoutLink.addEventListener('click', function(e) {
                e.preventDefault();
                const confirmLogout = confirm("Êtes-vous sûr de vouloir déconnecter ?");
                if (confirmLogout) {
                    window.location.href = this.href;
                }
            });
        }
    }
});




// js intefas inskripsyon

// Elements
const btnShowForm = document.getElementById('btnShowForm');
const formModal = document.getElementById('formModal');
const closeModal = document.getElementById('closeModal');
const cancelForm = document.getElementById('cancelForm');
const form = document.getElementById('inscriptionsForm');
const table = document.getElementById('tableEleves').getElementsByTagName('tbody')[0];

// Afficher modal
btnShowForm.addEventListener('click', () => {
  formModal.style.display = 'flex';
});

// Fermer modal
closeModal.addEventListener('click', () => {
  formModal.style.display = 'none';
});
cancelForm.addEventListener('click', () => {
  formModal.style.display = 'none';
});

// Ajouter un élève à la table
form.addEventListener('submit', (e) => {
  e.preventDefault();

  const data = Array.from(form.elements)
    .filter(el => el.tagName === "INPUT" || el.tagName === "SELECT")
    .map(el => el.value);

  const newRow = table.insertRow();
  data.forEach((value, index) => {
    const cell = newRow.insertCell();
    cell.textContent = value;
  });

  // Ajouter boutons action
  const actionCell = newRow.insertCell();
  actionCell.innerHTML = `
    <button class="btn btn-warning btn-sm"><i class="bi bi-pencil"></i></button>
    <button class="btn btn-danger btn-sm"><i class="bi bi-trash"></i></button>
  `;

  form.reset();
  formModal.style.display = 'none';
});

