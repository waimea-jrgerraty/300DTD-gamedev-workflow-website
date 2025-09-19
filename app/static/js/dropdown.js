document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach((dropdown) => {
        const button = dropdown.querySelector(".dropdown-btn");
        const menu = dropdown.querySelector(".dropdown-menu");

        button.addEventListener("click", (e) => {
            e.stopPropagation();

            // Close all other dropdowns first
            document.querySelectorAll(".dropdown-menu").forEach((m) => {
                if (m !== menu) m.style.display = "none";
            });

            // Toggle this one
            menu.style.display = menu.style.display === "block" ? "none" : "block";
        });
    });

    // Close dropdowns on outside click
    document.addEventListener("click", () => {
        document.querySelectorAll(".dropdown-menu").forEach((menu) => {
            menu.style.display = "none";
        });
    });
});