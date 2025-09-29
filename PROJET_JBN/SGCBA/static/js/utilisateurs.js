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

    // Ouvrir modal "Ajouter"
    btnShowUserForm.addEventListener("click", () => {
        userFormModal.classList.add("active");
    });
    closeUserModal.addEventListener("click", () => userFormModal.classList.remove("active"));
    cancelUserForm.addEventListener("click", () => userFormModal.classList.remove("active"));

    // Submit form "Ajouter"
    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const role = document.getElementById("role").value;
        const password = document.getElementById("password").value;
        const nom = document.getElementById("nom").value.trim();
        const prenom = document.getElementById("prenom").value.trim();

        const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=<>?]).{8,}$/;
        if (!passwordRegex.test(password)) {
            alert("⚠️ Mot de passe invalide !");
            return;
        }

        try {
            const response = await fetch("/api/utilisateurs/");
            const utilisateurs = await response.json();
            if (utilisateurs.some(u => u.username === username)) {
                alert("⚠️ Nom d’utilisateur déjà utilisé !");
                return;
            }
            if (utilisateurs.some(u => u.email === email)) {
                alert("⚠️ Email déjà utilisé !");
                return;
            }

            const data = { username, email, role, password, nom, prenom };
            const postResponse = await fetch("/api/utilisateurs/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(data)
            });

            if (postResponse.ok) {
                alert("✅ Utilisateur ajouté !");
                location.reload();
            } else {
                const err = await postResponse.json();
                alert("⚠️ Erreur: " + JSON.stringify(err));
            }

        } catch (error) {
            alert("🚨 Erreur réseau: " + error);
        }
    });

    // Charger utilisateurs
    async function loadUsers() {
        const response = await fetch("/api/utilisateurs/");
        const utilisateurs = await response.json();
        tableUsersBody.innerHTML = "";

        utilisateurs.forEach(utilisateur => {
            const newRow = tableUsersBody.insertRow();
            [utilisateur.nom, utilisateur.prenom, utilisateur.email, utilisateur.role, utilisateur.username]
                .forEach(val => {
                    const cell = newRow.insertCell();
                    cell.textContent = val;
                });

            // Actif
            const actifCell = newRow.insertCell();
            actifCell.className = "text-center";
            actifCell.innerHTML = `
                <label class="switch">
                    <input type="checkbox" ${utilisateur.actif ? "checked" : ""} data-id="${utilisateur.id}">
                    <span class="slider round"></span>
                </label>
            `;

            // Actions
            const actionCell = newRow.insertCell();
            actionCell.className = "text-center";
            actionCell.innerHTML = `
                <button class="btn btn-warning btn-sm btn-edit" data-id="${utilisateur.id}"><i class="fas fa-edit"></i></button>
                <button class="btn btn-danger btn-sm btn-delete" data-id="${utilisateur.id}"><i class="fas fa-trash-alt"></i></button>
            `;
        });

        // Event listener bouton modifier
        document.querySelectorAll(".btn-edit").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const userId = e.currentTarget.dataset.id;
                console.log("📝 Edit user ID:", userId); // Debug

                try {
                    const response = await fetch(`/api/utilisateurs/${userId}/`);
                    if (!response.ok) throw new Error("Utilisateur introuvable");
                    const utilisateur = await response.json();

                    // Remplir modal
                    document.getElementById("editUserId").value = utilisateur.id;
                    document.getElementById("editNom").value = utilisateur.nom;
                    document.getElementById("editPrenom").value = utilisateur.prenom;
                    document.getElementById("editEmail").value = utilisateur.email;
                    document.getElementById("editRole").value = utilisateur.role;
                    document.getElementById("editUsername").value = utilisateur.username;
                    document.getElementById("editActif").checked = utilisateur.actif;

                    // Afficher modal
                    editUserModal.classList.add("active");

                } catch (err) {
                    alert("🚨 Erreur: " + err);
                }
            });
        });

        // Fermer modal edit
        closeEditUserModal.addEventListener("click", () => editUserModal.classList.remove("active"));
        cancelEditUserForm.addEventListener("click", () => editUserModal.classList.remove("active"));

        // Submit form modification
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
                const putResponse = await fetch(`/api/utilisateurs/${userId}/`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
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

        // Event listener delete
        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const userId = e.currentTarget.dataset.id;
                if (!confirm("⚠️ Êtes-vous sûr de vouloir supprimer cet utilisateur ?")) return;

                try {
                    const deleteResponse = await fetch(`/api/utilisateurs/${userId}/`, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
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

        // Event listener toggle actif
        document.querySelectorAll("input[type=checkbox][data-id]").forEach(checkbox => {
            checkbox.addEventListener("change", async (e) => {
                const userId = e.currentTarget.dataset.id;
                const newStatus = e.currentTarget.checked;

                try {
                    const patchResponse = await fetch(`/api/utilisateurs/${userId}/`, {
                        method: "PATCH",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCookie("csrftoken")
                        },
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

    // Fonction CSRF
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
});
