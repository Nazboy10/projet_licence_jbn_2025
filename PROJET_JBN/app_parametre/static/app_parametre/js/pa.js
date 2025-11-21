document.addEventListener('DOMContentLoaded', () => {
    // --- Dropdown Profil ---
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

    // --- Gestion des switches ---
    document.querySelectorAll('.switch').forEach(switchEl => {
        const inputName = switchEl.dataset.name;
        const hiddenInput = document.getElementById(inputName);

        if (hiddenInput) {
            // Initialise l'état du switch selon la valeur du champ caché
            if (hiddenInput.value === '1') {
                switchEl.classList.add('on');
            } else {
                switchEl.classList.remove('on');
            }

            // Écouteur de clic
            switchEl.addEventListener('click', () => {
                switchEl.classList.toggle('on');
                hiddenInput.value = switchEl.classList.contains('on') ? '1' : '0';
            });

            // Support clavier (espace ou entrée)
            switchEl.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    switchEl.click();
                }
            });
        }
    });

    // --- Prévisualisation du logo ---
    const logoInput = document.getElementById('logoInput');
    const logoPreview = document.getElementById('logoPreview');

    if (logoInput && logoPreview) {
        logoInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) {
                logoPreview.innerHTML = '<i class="fas fa-image" style="color:var(--muted)"></i>';
                return;
            }
            if (!file.type.startsWith('image/')) {
                return;
            }
            const reader = new FileReader();
            reader.onload = (event) => {
                logoPreview.innerHTML = `<img src="${event.target.result}" alt="logo" style="max-width:100px; max-height:60px; object-fit:contain;">`;
            };
            reader.readAsDataURL(file);
        });
    }

    // --- Réinitialiser le formulaire ---
    window.resetForm = function() {
        if (!confirm('Réinitialiser les modifications non sauvegardées ?')) return;

        // Réinitialiser les champs du formulaire
        document.getElementById('formParam').reset();

        // Réinitialiser les switches selon leur valeur initiale (HTML)
        document.querySelectorAll('.switch').forEach(switchEl => {
            const inputName = switchEl.dataset.name;
            const hiddenInput = document.getElementById(inputName);
            if (hiddenInput) {
                // On suppose que la valeur HTML est la "valeur par défaut"
                if (hiddenInput.value === '1') {
                    switchEl.classList.add('on');
                } else {
                    switchEl.classList.remove('on');
                }
            }
        });

        // Réinitialiser la prévisualisation du logo
        if (logoPreview) {
            logoPreview.innerHTML = '<i class="fas fa-image" style="color:var(--muted)"></i>';
        }
    };
});