// ✅ Inscription.js - Ajout / Modification / Suppression (avec debug)
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
  if (!id) return alert("ID manquant pou modifier");
  try {
    const res = await fetch(`/inscription/get/${id}/`, { method: "GET" });
    const contentType = res.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      const text = await res.text();
      console.error("Expected JSON from get_inscription but got:", text);
      return alert("Erreur chargement: réponse non JSON (voir console).");
    }
    const data = await res.json();
    if (!res.ok) {
      console.error("Erreur get_inscription:", data);
      return alert("Erreur chargé: " + (data.error || "voir console"));
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
    form.classe.value = data.classe || "";
    form.telephone.value = data.telephone || "";
    form.email.value = data.email || "";
    form.nom_tuteur.value = data.nom_tuteur || "";
    form.tel_tuteur.value = data.tel_tuteur || "";
    form.action = `/inscription/modifier/${data.id}/`;
  } catch (err) {
    console.error("Erreur fetch get_inscription:", err);
    alert("Erreur lors du chargement des informations (voir console).");
  }
}

// Confirmation suppression
async function confirmDelete(id) {
  if (!confirm("⚠️ Eske w vle efase elèv sa a ?")) return;
  try {
    const res = await fetch(`/inscription/supprimer/${id}/`, {
      method: "POST",
      headers: { "X-CSRFToken": getCSRFToken() },
    });

    // Try parse JSON, else show text
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
      alert("✅ " + (data.message || "Suppression réussie"));
    } else {
      alert("❌ " + (data.error || "Erreur suppression (voir console)"));
      console.error("Suppression error:", data);
    }
  } catch (err) {
    console.error("Fetch delete error:", err);
    alert("❌ Une erreur est survenue côté client (voir console).");
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
        // Sèvè a retounen HTML (redirect oswa page) -> enprime li pou debug
        const text = await response.text();
        console.error("Response non-JSON from submit:", text);
        // Si sèvè te fè redirect oswa renvwaye HTML, nou ka swa al refresh, swa montre mesaj.
        // Ann eseye detekte si sa se yon page complète (kòmantè pou dev).
        alert("Warning: serveur renvoie HTML. Vérifiez console. Si l'inscription est bien créée, rafraîchissez la page.");
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
              <td><img src="${data.photo_url || '/static/images/default.png'}" width="50" class="rounded"></td>
              <td>${data.code_eleve}</td>
              <td>${data.nom}</td>
              <td>${data.prenom}</td>
              <td>${data.sexe}</td>
              <td>${data.adresse}</td>
              <td>${data.date_naissance || ''}</td>
              <td>${data.classe}</td>
              <td>${data.telephone}</td>
              <td>${data.email}</td>
              <td>${data.nom_tuteur}</td>
              <td>${data.tel_tuteur}</td>
              <td>${data.date_inscription || ''}</td>
              <td class="text-center">
                <button class="btn btn-warning btn-sm" data-id="${data.id}" onclick="loadAndEdit('${data.id}')">
                  <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-danger btn-sm" data-id="${data.id}" onclick="confirmDelete('${data.id}')">
                  <i class="bi bi-trash"></i>
                </button>
              </td>`;
          }
          alert("✅ Inscription modifié avec succès !");
        } else {
          // Ajout
          const newRow = document.createElement("tr");
          newRow.classList.add("eleve-row");
          newRow.innerHTML = `
            <td><img src="${data.photo_url || '/static/images/default.png'}" width="50" class="rounded"></td>
            <td>${data.code_eleve}</td>
            <td>${data.nom}</td>
            <td>${data.prenom}</td>
            <td>${data.sexe}</td>
            <td>${data.adresse}</td>
            <td>${data.date_naissance || ''}</td>
            <td>${data.classe}</td>
            <td>${data.telephone}</td>
            <td>${data.email}</td>
            <td>${data.nom_tuteur}</td>
            <td>${data.tel_tuteur}</td>
            <td>${data.date_inscription || ''}</td>
            <td class="text-center">
              <button class="btn btn-warning btn-sm" data-id="${data.id}" onclick="loadAndEdit('${data.id}')">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-danger btn-sm" data-id="${data.id}" onclick="confirmDelete('${data.id}')">
                <i class="bi bi-trash"></i>
              </button>
            </td>`;
          // prepend pou mete nouvo an tèt lis la
          if (eleveBody) eleveBody.prepend(newRow);
          alert("✅ Eleve inscrit avec succès !");
        }

        resetForm();
        modal.style.display = "none";
      } else {
        // Response 4xx/5xx avèk JSON
        console.error("Server error response:", data);
        alert("❌ " + (data.error || "Erreur côté serveur (voir console)"));
      }
    } catch (err) {
      console.error("Fetch submit error:", err);
      alert("❌ Une erreur est survenue côté client ! (voir console)");
    }
  });
}



// ✅ Pagination client-side (5 lignes par page)
// let currentPage = 1;
// const rowsPerPage = 5;
// let allRows = [];

// // Initialiser au chargement
// document.addEventListener("DOMContentLoaded", function () {
//   const tbody = document.querySelector("#tableEleves tbody");
//   if (!tbody) return;

//   // Sauvegarder uniquement les vraies lignes (pas le message "aucun élève")
//   allRows = Array.from(tbody.querySelectorAll("tr.eleve-row"));
//   renderPage(1);
// });

// // Afficher une page
// function renderPage(page) {
//   const tbody = document.querySelector("#tableEleves tbody");
//   if (!tbody) return;

//   const start = (page - 1) * rowsPerPage;
//   const end = start + rowsPerPage;
//   const pageRows = allRows.slice(start, end);

//   // Vider le tbody
//   tbody.innerHTML = "";

//   if (pageRows.length === 0) {
//     tbody.innerHTML = `<tr id="no-data"><td colspan="9" class="text-center">Aucun élève trouvé</td></tr>`;
//   } else {
//     pageRows.forEach(row => {
//       const clone = row.cloneNode(true);
//       tbody.appendChild(clone);
//     });
//   }

//   // Mettre à jour pagination
//   currentPage = page;
//   const totalPages = Math.ceil(allRows.length / rowsPerPage) || 1;
//   document.getElementById("btnPrev").disabled = page === 1;
//   document.getElementById("btnNext").disabled = page >= totalPages;
//   document.getElementById("pageInfo").textContent = `Page ${page} / ${totalPages}`;
// }

// // Recherche côté client (sans AJAX)
// document.getElementById("searchInput")?.addEventListener("input", function () {
//   const query = this.value.trim().toLowerCase();
//   const tbody = document.querySelector("#tableEleves tbody");
//   if (!tbody) return;

//   if (query.length < 2) {
//     // Restaurer toutes les lignes
//     const parser = new DOMParser();
//     const doc = parser.parseFromString(document.documentElement.outerHTML, "text/html");
//     allRows = Array.from(doc.querySelectorAll("#tableEleves tbody tr.eleve-row"));
//     renderPage(1);
//     return;
//   }

//   // Filtrer les lignes
//   const filtered = [];
//   allRows.forEach(row => {
//     const text = row.textContent.toLowerCase();
//     if (text.includes(query)) {
//       filtered.push(row);
//     }
//   });

//   allRows = filtered;
//   renderPage(1);
// });

// // Boutons pagination
// document.getElementById("btnPrev")?.addEventListener("click", () => {
//   if (currentPage > 1) renderPage(currentPage - 1);
// });

// document.getElementById("btnNext")?.addEventListener("click", () => {
//   const totalPages = Math.ceil(allRows.length / rowsPerPage);
//   if (currentPage < totalPages) renderPage(currentPage + 1);
// });