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

        // Confirmation déconnexion
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


// js interface inscription
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
const formNotes = document.getElementById('formNotes');
const notesFields = document.getElementById('notesFields');
const addNoteRow = document.getElementById('addNoteRow');
const successMessage = document.getElementById('successMessage');

// Liste matières predefini
const matieres = ["Maths", "Francais", "Physique", "Chimie", "Anglais"];

// Élèves prédefini pour test
const eleves = {
  "123": { nom: "Jean", prenom: "Dupont", classe: "Terminale" },
  "456": { nom: "Marie", prenom: "Curie", classe: "Première" }
};

// Fonction pour ajouter une ligne matière/note
function addNoteRowFunction() {
  const div = document.createElement('div');
  div.classList.add('row', 'g-2', 'mb-2', 'noteRow');
  let options = matieres.map(m => `<option value="${m}">${m}</option>`).join('');
  div.innerHTML = `
    <div class="col">
      <select class="form-select" name="matiere[]">
        ${options}
      </select>
    </div>
    <div class="col">
      <input type="number" class="form-control" name="note[]" placeholder="Entrer note">
    </div>
  `;
  notesFields.appendChild(div);
}

// Ouvrir modal
btnShowForm.addEventListener('click', () => {
  formModal.style.display = 'flex';
  step1.style.display = 'block';
  step2.style.display = 'none';
  codeError.style.display = 'none';
  inputCodeEleve.value = '';
  successMessage.style.display = 'none';
  notesFields.innerHTML = '';
  for(let i=0;i<2;i++){ addNoteRowFunction(); }
});

// Fermer modal
closeModal.addEventListener('click', () => formModal.style.display = 'none');
cancelForm.addEventListener('click', () => formModal.style.display = 'none');

// Vérifier code élève
btnVerifyCode.addEventListener('click', () => {
  const code = inputCodeEleve.value.trim();
  if(eleves[code]){
    codeError.style.display = 'none';
    step1.style.display = 'none';
    step2.style.display = 'block';
    nomEleve.textContent = eleves[code].nom;
    prenomEleve.textContent = eleves[code].prenom;
    classeEleve.textContent = eleves[code].classe;
  } else {
    codeError.style.display = 'block';
    step2.style.display = 'none';
  }
});

// Ajouter une ligne matière/note
addNoteRow.addEventListener('click', addNoteRowFunction);

// Enregistrement simulation
formNotes.addEventListener('submit', (e) => {
  e.preventDefault();
  successMessage.style.display = 'block';
  formNotes.reset();
  notesFields.innerHTML = '';
  for(let i=0;i<2;i++){ addNoteRowFunction(); }
});
