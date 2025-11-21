document.addEventListener("DOMContentLoaded", function () {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        // Si pa gen session => retounen login
        window.location.href = "/connexion/";
        return;
    }

    const role = user.role;

    // Default: kache tout meni
    document.querySelectorAll("nav ul li").forEach(li => li.style.display = "none");

    // Kontwòl nav selon wòl
    if (role === "directeur") {
        // Direktè wè tout
        document.querySelectorAll("nav ul li").forEach(li => li.style.display = "block");
    } 
    else if (role === "secretaire") {
        // Secretaire wè kèk meni sèlman
        ["menu-dashboard", "menu-inscription", "menu-eleve", "menu-presence"].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = "block";
        });
    } 
    else if (role === "censeur") {
        // Censeur wè lòt meni
        ["menu-dashboard", "menu-inscription", "menu-eleve", "menu-presence", "menu-note", "menu-bulletin"].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = "block";
        });
    }
});
