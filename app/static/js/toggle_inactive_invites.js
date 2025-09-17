document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("toggle-inactive");
    const invites = document.getElementById("invites");

    if (!toggle || !invites) return;

    toggle.addEventListener("change", () => {
        const children = invites.children;

        for (let child of children) {
            if (toggle.checked) {
                // When toggled ON: hidden_inactive → hidden
                if (child.classList.contains("hidden_inactive")) {
                    child.classList.remove("hidden_inactive");
                    child.classList.add("hidden");
                }
            } else {
                // When toggled OFF: hidden → hidden_inactive
                if (child.classList.contains("hidden")) {
                    child.classList.remove("hidden");
                    child.classList.add("hidden_inactive");
                }
            }
        }
    });
});