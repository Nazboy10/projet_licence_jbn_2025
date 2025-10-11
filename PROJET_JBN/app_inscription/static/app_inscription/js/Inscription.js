// ✅ Récupérer CSRF token
function getCSRFToken() {
  return document.cookie.split(";")
    .find(c => c.trim().startsWith("csrftoken="))
    ?.split("=")[1];
}

// ✅ Aperçu photo (selon demann ou — sèlman non fichye a)
const photoInput = document.getElementById("photoInput");
const photoPreview = document.getElementById("photoPreview");

if (photoInput) {
  photoInput.addEventListener("change", () => {
    const file = photoInput.files[0];
    if (file) {
      // montre sèlman non fichye a
      photoPreview.src = "{% static 'images/default.png' %}";
    }
  });
}

// ✅ Modal gestion
const modal = document.getElementById("formModal");
const btnShowForm = document.getElementById("btnShowForm");
const closeModal = document.getElementById("closeModal");
const cancelForm = document.getElementById("cancelForm");

btnShowForm.onclick = () => modal.style.display = "flex";
closeModal.onclick = () => modal.style.display = "none";
cancelForm.onclick = () => modal.style.display = "none";

// ✅ Soumission du formulaire san rechargement
const form = document.getElementById("inscriptionForm");
const eleveBody = document.getElementById("eleveBody");

if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const csrfToken = getCSRFToken();

    const response = await fetch("/inscription/ajouter/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
      body: formData,
    });

    if (response.ok) {
      const data = await response.json(); // Django doit renvoyer JSON

      // ajoute nouvo elèv nan tablo a
      const newRow = document.createElement("tr");
      newRow.innerHTML = `
        <td><img src="${data.photo_url}" width="50"></td>
        <td>${data.code_eleve}</td>
        <td>${data.nom}</td>
        <td>${data.prenom}</td>
        <td>${data.sexe}</td>
        <td>${data.adresse}</td>
        <td>${data.date_naissance}</td>
        <td>${data.classe}</td>
        <td>${data.telephone}</td>
        <td>${data.email}</td>
        <td>${data.nom_tuteur}</td>
        <td>${data.tel_tuteur}</td>
        <td>${data.date_inscription}</td>
        <td class="text-center">
          <button class="btn btn-warning btn-sm"><i class="bi bi-pencil"></i></button>
          <button class="btn btn-danger btn-sm" onclick="confirmDelete('${data.id}')"><i class="bi bi-trash"></i></button>
        </td>
      `;
      eleveBody.prepend(newRow); // ajoute elèv la anwo lis la

      alert("✅ Élève inscrit avec succès !");
      form.reset();
      modal.style.display = "none";
      photoPreview.src = "{% static 'images/default.png' %}";
    } else {
      alert("❌ Erreur lors de l’inscription !");
    }
  });
}

// ✅ Confirmation suppression
function confirmDelete(id) {
  if (confirm("⚠️ Eske w vle efase elèv sa a ?")) {
    fetch(`/inscription/supprimer/${id}/`, {
      method: "POST",
      headers: { "X-CSRFToken": getCSRFToken() },
    }).then(() => {
      document.querySelector(`button[onclick="confirmDelete('${id}')"]`)
        ?.closest("tr")
        ?.remove();
    });
  }
}

// ✅ Gérer affichage (10/25/50)
const selectAffichage = document.getElementById("nbAffichage");
if (selectAffichage) {
  selectAffichage.addEventListener("change", () => {
    const rows = eleveBody.querySelectorAll("tr");
    rows.forEach((row, index) => {
      row.style.display = index < parseInt(selectAffichage.value) ? "" : "none";
    });
  });
}


document.addEventListener('DOMContentLoaded', () => {
  const editButtons = document.querySelectorAll('.btn-edit');
  const form = document.getElementById('editForm');
  const modal = document.getElementById('editModal');

  editButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      fetch(`/inscription/get/${id}/`)
        .then(response => response.json())
        .then(data => {
          form.action = `/inscription/modifier/${id}/`;
          document.getElementById('nom').value = data.nom;
          document.getElementById('prenom').value = data.prenom;
          document.getElementById('sexe').value = data.sexe;
          document.getElementById('adresse').value = data.adresse;
          document.getElementById('classe').value = data.classe;
          document.getElementById('date_naissance').value = data.date_naissance;
          document.getElementById('telephone').value = data.telephone;
          document.getElementById('email').value = data.email;
          document.getElementById('nom_tuteur').value = data.nom_tuteur;
          document.getElementById('tel_tuteur').value = data.tel_tuteur;
          modal.style.display = 'block';
        });
    });
  });

  document.getElementById('closeModal').addEventListener('click', () => {
    modal.style.display = 'none';
  });

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
      method: 'POST',
      body: formData,
    })
    .then(res => res.json())
    .then(data => {
      if (data.message) {
        alert('✅ ' + data.message);
        location.reload();
      } else {
        alert('❌ Erè pandan modification');
      }
    });
  });
});


