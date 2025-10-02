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

// Toggle switches and sync hidden inputs
document.querySelectorAll('.switch').forEach(s => {
  const name = s.dataset.name;
  const hidden = name ? document.getElementById(name) : null;
  if(hidden){
    hidden.value = s.classList.contains('on') ? '1' : '0';
  }
  s.addEventListener('click', () => {
    s.classList.toggle('on');
    if(hidden) hidden.value = s.classList.contains('on') ? '1' : '0';
  });
  s.addEventListener('keypress', (e) => {
    if(e.key === 'Enter' || e.key === ' ') { e.preventDefault(); s.click(); }
  });
});

// Logo preview
const logoInput = document.getElementById('logoInput');
const logoPreview = document.getElementById('logoPreview');
logoInput && logoInput.addEventListener('change', (e) => {
  const f = e.target.files && e.target.files[0];
  if(!f) { logoPreview.innerHTML = '<i class="fas fa-image" style="color:var(--muted)"></i>'; return; }
  if(!f.type.startsWith('image/')) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    logoPreview.innerHTML = '<img src="'+ev.target.result+'" alt="logo">';
  }
  reader.readAsDataURL(f);
});

function resetForm(){
  if(!confirm('Réinitialiser les modifications non sauvegardées ?')) return;
  document.getElementById('formParam').reset();
  document.querySelectorAll('.switch').forEach(s => {
    s.classList.remove('on');
    const hidden = s.dataset.name ? document.getElementById(s.dataset.name) : null;
    if(hidden) hidden.value = '0';
  });
  document.querySelectorAll('.switch.on').forEach(s => {
    const hidden = s.dataset.name ? document.getElementById(s.dataset.name) : null;
    if(hidden) hidden.value = '1';
  });
  logoPreview.innerHTML = '<i class="fas fa-image" style="color:var(--muted)"></i>';
}
