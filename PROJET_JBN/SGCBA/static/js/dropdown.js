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


