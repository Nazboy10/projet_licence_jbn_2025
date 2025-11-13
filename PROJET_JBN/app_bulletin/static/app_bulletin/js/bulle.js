document.addEventListener('DOMContentLoaded', () => {

    // === Gestion du dropdown profil (inchangé) ===
    const toggle = document.getElementById('profileDropdownToggle');
    const dropdown = document.getElementById('profileDropdown');

    if (toggle && dropdown) {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', () => {
            dropdown.style.display = 'none';
        });

        dropdown.addEventListener('click', (e) => {
            e.stopPropagation();
        });

        const logoutLink = dropdown.querySelector("a");
        if (logoutLink) {
            logoutLink.addEventListener('click', function(e) {
                e.preventDefault();
                const confirmLogout = confirm("Êtes-vous sûr merd de vouloir déconnecter ?");
                if (confirmLogout) {
                    window.location.href = this.href;
                }
            });
        }
    }

    // === Éléments du bulletin ===
    const tbody = document.querySelector("#listeBulletin tbody");
    const bulletinPage = document.getElementById('bulletinPage');
    const listeContainer = document.getElementById('listeContainer');
    const logoCachetContainer = document.getElementById('logoCachetContainer');
    const btnAfficherFormulaire = document.getElementById('btnAfficherFormulaire');
    const formulairePage = document.getElementById('formulairePage');
    const inputCodeForm = document.getElementById('inputCodeForm');
    const btnValiderForm = document.getElementById('btnValiderForm');
    const btnRetourForm = document.getElementById('btnRetourForm');

    // === Fonction principale : afficher bulletin depuis l'API ===
    async function chargerEtAfficherBulletin(codeEleve) {
        try {
            const res = await fetch(`/bulletin/api/bulletin/?code=${encodeURIComponent(codeEleve)}`);
            const data = await res.json();

            if (!res.ok) {
                alert(data.erreur || "Élève non trouvé ou aucune note disponible.");
                return;
            }

            const { eleve, notes, total_pondere, moyenne, mention } = data;
            listeContainer.style.display = 'none';
            formulairePage.style.display = 'none';
            btnAfficherFormulaire.style.display = 'inline-block';

            const lignesNotes = notes.map(n => 
                `<tr><td>${n.matiere}</td><td>${n.coef}</td><td>${n.note}</td><td>${n.pondere.toFixed(2)}</td></tr>`
            ).join('');

           bulletinPage.innerHTML = `
    <img id="bulletinLogo" src="/static/icone/CBA.png" alt="Logo École" style="max-width:150px; margin-bottom:10px;">
    <h3>Bulletin de ${eleve.prenom} ${eleve.nom} | Classe: ${eleve.classe}</h3>
    <table border="1" style="width:100%; margin-top:10px; border-collapse: collapse;">
        <thead>
            <tr><th>Matière</th><th>Coef</th><th>Note</th><th>Pondérée</th></tr>
        </thead>
        <tbody>
            ${lignesNotes}
        </tbody>
        <tfoot>
            <tr><td colspan="3">Total pondéré</td><td>${total_pondere.toFixed(2)}</td></tr>
            <tr><td colspan="3">Moyenne</td><td>${moyenne} (${mention})</td></tr>
        </tfoot>
    </table>
    <img id="bulletinCachet" src="/static/image/cachet.png" alt="Cachet Directeur" style="max-width:150px; margin-top:10px;">
    <div style="margin-top:15px; display:flex; gap:10px; flex-wrap:wrap;">
        <button onclick="window.print()">🖨️ Imprimer / PDF</button>
        <button id="btnEnregistrerBulletin" data-code="${eleve.code}" data-periode="${data.periode || '1er_trimestre'}">
            💾 Enregistrer dans la base
        </button>
        <button id="btnRetour">⬅️ Retour à la liste</button>
    </div>
`;

            // Réinitialiser la zone de chargement d'images
            logoCachetContainer.innerHTML = `
                <input type="file" id="logoChoix" accept="image/*" style="display:none;">
                <input type="file" id="cachetChoix" accept="image/*" style="display:none;">
            `;

            // Gérer le retour
            document.getElementById('btnRetour').addEventListener('click', () => {
                bulletinPage.innerHTML = '';
                logoCachetContainer.innerHTML = '';
                listeContainer.style.display = 'block';
            });


             
// ✅ NOUVEAU : Gérer l'enregistrement
document.getElementById('btnEnregistrerBulletin')?.addEventListener('click', async () => {
    const code = document.getElementById('btnEnregistrerBulletin').dataset.code;
    const periode = document.getElementById('btnEnregistrerBulletin').dataset.periode;

    try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                          document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/, "$1");

        const res = await fetch('/bulletin/api/enregistrer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ code, periode })
        });

        const result = await res.json();
        if (res.ok) {
            alert('✅ Bulletin enregistré avec succès !');
        } else {
            alert('❌ Erreur : ' + (result.erreur || 'Échec'));
        }
    } catch (err) {
        console.error(err);
        alert('Erreur réseau lors de l’enregistrement.');
    }
});




            // Gérer le changement de logo/cachet
            const logoInput = document.getElementById('logoChoix');
            const cachetInput = document.getElementById('cachetChoix');

            if (logoInput) {
                logoInput.addEventListener('change', e => {
                    if (e.target.files[0]) {
                        const url = URL.createObjectURL(e.target.files[0]);
                        document.getElementById('bulletinLogo').src = url;
                    }
                });
            }

            if (cachetInput) {
                cachetInput.addEventListener('change', e => {
                    if (e.target.files[0]) {
                        const url = URL.createObjectURL(e.target.files[0]);
                        document.getElementById('bulletinCachet').src = url;
                    }
                });
            }

        } catch (err) {
            console.error("Erreur de chargement du bulletin :", err);
            alert("Erreur de connexion au serveur. Veuillez réessayer.");
        }
    }

    // === Gestion des clics ===
    tbody.addEventListener('click', e => {
        if (e.target.classList.contains('btnRechercher')) {
            const row = e.target.closest('tr');
            const code = row?.children[0]?.textContent?.trim();
            if (code) {
                chargerEtAfficherBulletin(code);
                logoCachetContainer.innerHTML = '';
                btnAfficherFormulaire.style.display = 'none';
            }
        }
    });

    btnAfficherFormulaire.addEventListener('click', () => {
        formulairePage.style.display = 'block';
        inputCodeForm.value = '';
        inputCodeForm.focus();
        listeContainer.style.display = 'none';
        bulletinPage.innerHTML = '';
        btnAfficherFormulaire.style.display = 'none';
    });

    btnValiderForm.addEventListener('click', () => {
        const code = inputCodeForm.value.trim();
        if (!code) {
            alert("Veuillez entrer le code de l'élève.");
            return;
        }
        chargerEtAfficherBulletin(code);
    });

    btnRetourForm.addEventListener('click', () => {
        formulairePage.style.display = 'none';
        listeContainer.style.display = 'block';
        btnAfficherFormulaire.style.display = 'inline-block';
    });

});