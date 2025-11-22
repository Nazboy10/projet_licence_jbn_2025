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
                Swal.fire({
                  title: 'Déconnexion',
                  text: "Êtes-vous sûr de  vouloir déconnecter ?",
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


//upload photo de profil

function uploadPhoto() {
    const user = JSON.parse(localStorage.getItem("user"));
    const fileInput = document.getElementById("photoInput");

    if (!fileInput.files.length) return;

    const formData = new FormData();
    formData.append("photo", fileInput.files[0]);
    formData.append("user_id", user.id);  // voye id itilizatè

    // 👉 Ranmase CSRF token la
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/upload-photo/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken  // ajoute CSRF token nan headers
        },
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        if (data.photo_url) {
            // ajoute timestamp pou evite cache
            document.querySelector(".user-avatar img").src = data.photo_url + "?t=" + new Date().getTime();
            alert("Photo de profil mise à jour !");
        } else {
            alert("Erreur lors de la mise à jour de la photo");
        }
    })
    .catch(err => console.error(err));
}



// Fonksyon pou jwenn CSRF
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
