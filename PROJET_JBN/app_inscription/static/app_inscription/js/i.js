// ...existing code...
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
});
// ...existing code...

// ✅ Inscription.js - Ajout / Modification / Suppression (avec SweetAlert2)
// Ranmase CSRF token
function getCSRFToken() {
  return document.cookie
    .split(";")
    .find(c => c.trim().startsWith("csrftoken="))
    ?.split("=")[1] || null;
}

// Sélection DOM (fallback si tbody pa gen id)
const form = document.getElementById("inscriptionForm");
const eleveBody = document.getElementById("eleveBody") || document.querySelector("tbody");
const modal = document.getElementById("formModal");
const btnShowForm = document.getElementById("btnShowForm");
const closeModal = document.getElementById("closeModal");
const cancelForm = document.getElementById("cancelForm");

// Ouvrir modal pour ajouter
if (btnShowForm) {
  btnShowForm.addEventListener("click", () => {
    resetForm();
    document.getElementById("formTitle").textContent = "Formulaire Inscription";
    document.getElementById("btnSubmit").textContent = "Inscrire";
    modal.style.display = "block";
  });
}

// Fermer modal
[closeModal, cancelForm].forEach(btn => {
  if (btn) btn.addEventListener("click", () => {
    modal.style.display = "none";
    resetForm();
  });
});

// Reset form
function resetForm() {
  if (!form) return;
  form.reset();
  // Assure ke dataset.url defini sou tag form nan HTML
  if (form.dataset && form.dataset.url) {
    form.action = form.dataset.url;
  }
  if (form.eleve_id) form.eleve_id.value = "";
  const btn = document.getElementById("btnSubmit");
  if (btn) btn.textContent = "Inscrire";
}

// Récupérer données d'un élève et ouvrir modal pour modifier
// (fonction globale pou kapab rele depi onclick nan HTML: onclick="loadAndEdit('ID')")
async function loadAndEdit(id) {
  if (!id) {
    Swal.fire({icon:'warning', title:'ID manquant', text:'ID manquant pou modifier'});
    return;
  }
  try {
    const res = await fetch(`/inscription/get/${id}/`, { method: "GET" });
    const contentType = res.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      const text = await res.text();
      console.error("Expected JSON from get_inscription but got:", text);
      Swal.fire({icon:'error', title:'Erreur', text:'Réponse serveur non JSON. Voir console.'});
      return;
    }
    const data = await res.json();
    if (!res.ok) {
      console.error("Erreur get_inscription:", data);
      Swal.fire({icon:'error', title:'Erreur', text: data.error || 'Erreur chargement (voir console)'});
      return;
    }

    // Remplir form
    modal.style.display = "block";
    document.getElementById("formTitle").textContent = "Modifier Élève";
    document.getElementById("btnSubmit").textContent = "Modifier";

    form.eleve_id.value = data.id || "";
    form.nom.value = data.nom || "";
    form.prenom.value = data.prenom || "";
    form.sexe.value = data.sexe || "";
    form.adresse.value = data.adresse || "";
    form.date_naissance.value = data.date_naissance || "";
    form.lieu_naissance.value = data.lieu_naissance || "";
    form.classe.value = data.classe || "";
    form.telephone.value = data.telephone || "";
    form.email.value = data.email || "";
    form.nom_tuteur.value = data.nom_tuteur || "";
    form.tel_tuteur.value = data.tel_tuteur || "";
    form.action = `/inscription/modifier/${data.id}/`;
  } catch (err) {
    console.error("Erreur fetch get_inscription:", err);
    Swal.fire({icon:'error', title:'Erreur', text:'Erreur lors du chargement des informations (voir console).'});
  }
}

// Confirmation suppression
async function confirmDelete(id) {
  const result = await Swal.fire({
    text: '⚠️ est-ce que vous voulez supprimer?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Oui',
    cancelButtonText: 'Non'
  });

  if (!result.isConfirmed) return;

  try {
    const res = await fetch(`/inscription/supprimer/${id}/`, {
      method: "POST",
      headers: { "X-CSRFToken": getCSRFToken() },
    });

    const ct = res.headers.get("content-type") || "";
    let data;
    if (ct.includes("application/json")) {
      data = await res.json();
    } else {
      const text = await res.text();
      console.warn("Delete response non-json:", text);
      data = { message: text };
    }

    if (res.ok) {
      const btn = document.querySelector(`button[data-id='${id}']`);
      const row = btn ? btn.closest("tr") : null;
      if (row) row.remove();
      Swal.fire({icon:'success', title:'Supprimé', text: data.message || 'Suppression réussie', timer:1500, showConfirmButton:false});
      
    } else {
      console.error("Suppression error:", data);
      Swal.fire({icon:'error', title:'Erreur', text: data.error || 'Erreur suppression (voir console)'});
    }
  } catch (err) {
    console.error("Fetch delete error:", err);
    Swal.fire({icon:'error', title:'Erreur', text:'Une erreur est survenue côté client (voir console).'});
  }
}





// Soumission formulaire (ajout / modif)
if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const csrfToken = getCSRFToken();
    const eleveId = formData.get("eleve_id");
    const url = eleveId ? `/inscription/modifier/${eleveId}/` : (form.dataset.url || form.action);

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
      });

      const contentType = response.headers.get("content-type") || "";
      let data = null;

      if (contentType.includes("application/json")) {
        data = await response.json();
      } else {
        const text = await response.text();
        console.error("Response non-JSON from submit:", text);
        Swal.fire({icon:'warning', title:'Réponse serveur', text:'Serveur renvoie HTML. Vérifiez console.'});
        return;
      }

      if (response.ok) {
        // Si modification
        if (eleveId) {
          const btn = document.querySelector(`button[data-id='${eleveId}']`);
          const row = btn ? btn.closest("tr") : null;
          
          if (row) {
            row.className = "eleve-row";
            row.innerHTML = `
              <td class="text-center"><img src="${data.photo_url || '/static/images/default.png'}" width="50" class="rounded"></td>
              <td>${data.code_eleve}</td>
              <td>${data.nom}</td>
              <td>${data.prenom}</td>
              <td>${data.sexe}</td>
              <td>${data.classe}</td>
              <td>${data.date_inscription || ''}</td>
              <td>${data.annee_academique || ''}</td>
              <td class="text-center">
                <div class="d-flex justify-content-center gap-2">
                  <button class="btn btn-sm btn-outline-primary" onclick="showDetails('${data.id}')"><i class="bi bi-eye"></i></button>
                  <button class="btn btn-warning btn-sm" data-id="${data.id}" onclick="editEleve('${data.id}', '${escapeHtml(data.nom)}', '${escapeHtml(data.prenom)}', '${escapeHtml(data.sexe)}', '${escapeHtml(data.adresse)}', '${data.date_naissance || ''}', '${escapeHtml(data.classe)}', '${escapeHtml(data.telephone)}', '${escapeHtml(data.email)}', '${escapeHtml(data.nom_tuteur)}', '${escapeHtml(data.tel_tuteur)}')"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-danger btn-sm" data-id="${data.id}" onclick="confirmDelete('${data.id}')"><i class="bi bi-trash"></i></button>
                </div>
              </td>`;
          }
          Swal.fire({icon:'success', title:'Modifié', text:'Inscription modifié avec succès', timer:1500, showConfirmButton:false});
        } else {
          // Ajout
          const newRow = document.createElement("tr");
          newRow.classList.add("eleve-row");
          newRow.innerHTML = `
            <td class="text-center"><img src="${data.photo_url || '/static/images/default.png'}" width="50" class="rounded"></td>
            <td>${data.code_eleve}</td>
            <td>${data.nom}</td>
            <td>${data.prenom}</td>
            <td>${data.sexe}</td>
            <td>${data.classe}</td>
            <td>${data.date_inscription || ''}</td>
            <td>${data.annee_academique || ''}</td>
            <td class="text-center">
              <div class="d-flex justify-content-center gap-2">
                <button class="btn btn-sm btn-outline-primary" onclick="showDetails('${data.id}')"><i class="bi bi-eye"></i></button>
                <button class="btn btn-warning btn-sm" data-id="${data.id}" onclick="editEleve('${data.id}', '${escapeHtml(data.nom)}', '${escapeHtml(data.prenom)}', '${escapeHtml(data.sexe)}', '${escapeHtml(data.adresse)}', '${data.date_naissance || ''}', '${escapeHtml(data.classe)}', '${escapeHtml(data.telephone)}', '${escapeHtml(data.email)}', '${escapeHtml(data.nom_tuteur)}', '${escapeHtml(data.tel_tuteur)}')"><i class="bi bi-pencil"></i></button>
                <button class="btn btn-danger btn-sm" data-id="${data.id}" onclick="confirmDelete('${data.id}')"><i class="bi bi-trash"></i></button>
              </div>
            </td>`;
          if (eleveBody) eleveBody.prepend(newRow);
          Swal.fire({icon:'success', title:'Ajouté', text:'Élève inscrit avec succès', timer:1500, showConfirmButton:false});
        }

      

        resetForm();
        modal.style.display = "none";
      } else {
        console.error("Server error response:", data);
        Swal.fire({icon:'error', title:'Erreur', text: data.error || 'Erreur côté serveur (voir console)'});
      }
    } catch (err) {
      console.error("Fetch submit error:", err);
      Swal.fire({icon:'error', title:'Erreur', text:'Une erreur est survenue côté client (voir console).'});
    }
  });
  
}

// util helper : échapper simple pour insertion dans attribut onclick
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str).replace(/'/g,"\\'").replace(/"/g,'&quot;').replace(/\n/g,' ');
}
// ...existing code...


