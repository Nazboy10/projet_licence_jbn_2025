document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("utilisateursForm");
    const btnShowUserForm = document.getElementById("btnShowUserForm");
    const userFormModal = document.getElementById("userFormModal");
    const closeUserModal = document.getElementById("closeUserModal");
    const cancelUserForm = document.getElementById("cancelUserForm");
    const tableUsersBody = document.getElementById("tableUsersBody");
    const editUserModal = document.getElementById("editUserFormModal");
    const closeEditUserModal = document.getElementById("closeEditUserModal");
    const cancelEditUserForm = document.getElementById("cancelEditUserForm");
    const editUserForm = document.getElementById("editUserForm");

    // 🔐 Helper: récupère CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ⚙️ Helper global fetch (ajoute credentials + csrf + token otomatikman)
async function djangoFetch(url, options = {}) {
    const csrftoken = getCookie("csrftoken");
    const defaults = {
        credentials: "same-origin", // kenbe session
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    };
    return fetch(url, { ...defaults, ...options });
}



    // ----------------------------- //
    // 📋 GESTION FORMULAIRE AJOUT
    // ----------------------------- //
    btnShowUserForm.addEventListener("click", () => {
        clearFieldErrors();
        userFormModal.classList.add("active");
    });
    closeUserModal.addEventListener("click", () => {
        clearFieldErrors();
        userFormModal.classList.remove("active");
    });
    cancelUserForm.addEventListener("click", () => {
        clearFieldErrors();
        userFormModal.classList.remove("active");
    });

    form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const role = document.getElementById("role").value;
    const password = document.getElementById("password").value;
    const nom = document.getElementById("nom").value.trim();
    const prenom = document.getElementById("prenom").value.trim();

    clearFieldErrors();

    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=<>?]).{8,}$/;
    if (!passwordRegex.test(password)) {
        showFieldError('password', '⚠️ Mot de passe invalide : au moins 8 caractères, une majuscule, un chiffre et un caractère spécial.');
        return;
    }

    try {
        // 🔐 Récupération token JWT depuis localStorage
        const token = localStorage.getItem("token");
        if (!token) {
            alert("⚠️ Vous devez être connecté pour ajouter un utilisateur.");
            return;
        }

        // 🔐 Vérification utilisateurs existants
        const response = await djangoFetch("/api/utilisateurs/", { method: "GET" });
        const utilisateurs = await response.json();

        console.log("📦 Réponse API utilisateurs:", utilisateurs);

        let usersList = [];
        if (Array.isArray(utilisateurs)) {
            usersList = utilisateurs;
        } else if (utilisateurs && Array.isArray(utilisateurs.results)) {
            usersList = utilisateurs.results;
        } else {
            alert("⚠️ L’API n’a pas retourné une liste valide.");
            return;
        }

        if (usersList.some(u => u.username === username)) {
            showFieldError('username', "⚠️ Nom d’utilisateur déjà utilisé !");
            return;
        }
        if (usersList.some(u => u.email === email)) {
            showFieldError('email', "⚠️ Email déjà utilisé !");
            return;
        }

        const data = { username, email, role, password, nom, prenom };

        // 🔐 POST avec token JWT
        const postResponse = await djangoFetch("/api/utilisateurs/", {
            method: "POST",
            body: JSON.stringify(data),
        });

        if (postResponse.ok) {
            alert("✅ Utilisateur ajouté !");
            location.reload();
        } else {
            let err = {};
            try {
                err = await postResponse.json();
            } catch (e) {
                document.getElementById('userFormErrors').textContent = '⚠️ Erreur serveur inattendue.';
                return;
            }

            if (typeof err === 'string') {
                alert('⚠️ ' + err);
            } else if (err) {
                for (const key in err) {
                    const val = err[key];
                    const message = Array.isArray(val) ? val.join(' ; ') : (typeof val === 'object' ? JSON.stringify(val) : val);
                    if (['password','username','email','nom','prenom'].includes(key)) {
                        showFieldError(key, message);
                    } else {
                        alert(key + ': ' + message);
                    }
                }
            }
        }

    } catch (error) {
        alert("🚨 Erreur réseau: " + error);
    }
});


    // ----------------------------- //
    // 📋 CHARGER ET GÉRER UTILISATEURS
    // ----------------------------- //
    async function loadUsers() {
        const response = await djangoFetch("/api/utilisateurs/", { method: "GET" });
        const utilisateurs = await response.json();
        const usersList = Array.isArray(utilisateurs) ? utilisateurs : utilisateurs.results || [];

        tableUsersBody.innerHTML = "";

        usersList.forEach(utilisateur => {
            const newRow = tableUsersBody.insertRow();
            [utilisateur.nom, utilisateur.prenom, utilisateur.email, utilisateur.role, utilisateur.username]
                .forEach(val => {
                    const cell = newRow.insertCell();
                    cell.textContent = val;
                });

            const actifCell = newRow.insertCell();
            actifCell.className = "text-center";
            actifCell.innerHTML = `
                <label class="switch">
                    <input type="checkbox" ${utilisateur.actif ? "checked" : ""} data-id="${utilisateur.id}">
                    <span class="slider round"></span>
                </label>
            `;

            const actionCell = newRow.insertCell();
            actionCell.className = "text-center";
            actionCell.innerHTML = `
                <button class="btn btn-warning btn-sm btn-edit" data-id="${utilisateur.id}"><i class="fas fa-edit"></i></button>
                <button class="btn btn-danger btn-sm btn-delete" data-id="${utilisateur.id}"><i class="fas fa-trash-alt"></i></button>
            `;
        });

        // 🛠 Bouton modifier
        document.querySelectorAll(".btn-edit").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const userId = e.currentTarget.dataset.id;
                try {
                    const response = await djangoFetch(`/api/utilisateurs/${userId}/`, { method: "GET" });
                    if (!response.ok) throw new Error("Utilisateur introuvable");
                    const utilisateur = await response.json();

                    document.getElementById("editUserId").value = utilisateur.id;
                    document.getElementById("editNom").value = utilisateur.nom;
                    document.getElementById("editPrenom").value = utilisateur.prenom;
                    document.getElementById("editEmail").value = utilisateur.email;
                    document.getElementById("editRole").value = utilisateur.role;
                    document.getElementById("editUsername").value = utilisateur.username;
                    document.getElementById("editActif").checked = utilisateur.actif;

                    editUserModal.classList.add("active");
                } catch (err) {
                    alert("🚨 Erreur: " + err);
                }
            });
        });

        closeEditUserModal.addEventListener("click", () => editUserModal.classList.remove("active"));
        cancelEditUserForm.addEventListener("click", () => editUserModal.classList.remove("active"));

        editUserForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const userId = document.getElementById("editUserId").value;
            const data = {
                nom: document.getElementById("editNom").value.trim(),
                prenom: document.getElementById("editPrenom").value.trim(),
                email: document.getElementById("editEmail").value.trim(),
                role: document.getElementById("editRole").value,
                username: document.getElementById("editUsername").value.trim(),
                actif: document.getElementById("editActif").checked,
            };

            try {
                const putResponse = await djangoFetch(`/api/utilisateurs/${userId}/`, {
                    method: "PUT",
                    body: JSON.stringify(data)
                });

                if (putResponse.ok) {
                    alert("✅ Utilisateur modifié !");
                    editUserModal.classList.remove("active");
                    loadUsers();
                } else {
                    const err = await putResponse.json();
                    alert("⚠️ Erreur: " + JSON.stringify(err));
                }
            } catch (err) {
                alert("🚨 Erreur réseau: " + err);
            }
        });

        // 🗑 Supprimer
        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const userId = e.currentTarget.dataset.id;
                if (!confirm("⚠️ Êtes-vous sûr de vouloir supprimer cet utilisateur ?")) return;

                try {
                    const deleteResponse = await djangoFetch(`/api/utilisateurs/${userId}/`, {
                        method: "DELETE"
                    });

                    if (deleteResponse.ok) {
                        alert("✅ Utilisateur supprimé !");
                        loadUsers();
                    } else {
                        alert("⚠️ Erreur lors de la suppression !");
                    }
                } catch (err) {
                    alert("🚨 Erreur réseau: " + err);
                }
            });
        });

        // ✅ Toggle actif
        document.querySelectorAll("input[type=checkbox][data-id]").forEach(checkbox => {
            checkbox.addEventListener("change", async (e) => {
                const userId = e.currentTarget.dataset.id;
                const newStatus = e.currentTarget.checked;

                try {
                    const patchResponse = await djangoFetch(`/api/utilisateurs/${userId}/`, {
                        method: "PATCH",
                        body: JSON.stringify({ actif: newStatus })
                    });

                    if (!patchResponse.ok) {
                        alert("⚠️ Erreur lors de la mise à jour du statut !");
                        e.currentTarget.checked = !newStatus;
                    }
                } catch (err) {
                    alert("🚨 Erreur réseau: " + err);
                    e.currentTarget.checked = !newStatus;
                }
            });
        });
    }

    loadUsers();

    // Helpers d'erreurs
    function showFieldError(field, message) {
        const el = document.getElementById(`error-${field}`);
        if (el) el.textContent = message;
    }

    function clearFieldErrors() {
        ['password','username','email','nom','prenom'].forEach(f => {
            const el = document.getElementById(`error-${f}`);
            if (el) el.textContent = '';
        });
        const general = document.getElementById('userFormErrors');
        if (general) general.innerHTML = '';
    }

    ['password','username','email','nom','prenom'].forEach(f => {
        const input = document.getElementById(f);
        if (input) input.addEventListener('input', () => {
            const el = document.getElementById(`error-${f}`);
            if (el) el.textContent = '';
        });
    });

    






});
