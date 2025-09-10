document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.getElementById("p-open-add-user");
    const modal = document.getElementById("p-add-user-modal");
    const cancelBtn = document.getElementById("p-cancel-add-user");
    const confirmBtn = document.getElementById("p-confirm-add-user");
    const input = document.getElementById("p-member-input");
    const errorOut = document.getElementById("p-add-user-error");

    // Read IDs from dataset
    const PROJECT_ID = openBtn.dataset.projectId;

    async function assignUserToProject(username) {
        const res = await fetch(`/api/projects/${PROJECT_ID}/assign`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username })
        });
        if (!res.ok) {
            const j = await res.json().catch(() => ({}));
            throw new Error(j.error || "Failed to assign user");
        }
    }

    openBtn.addEventListener("click", async () => {
        errorOut.textContent = "";
        input.value = "";
        try {
            modal.showModal();
            input.focus();
        } catch (err) {
            errorOut.textContent = err.message;
            modal.showModal();
        }
    });

    cancelBtn.addEventListener("click", () => modal.close());
    modal.addEventListener("cancel", (e) => { e.preventDefault(); modal.close(); });

    confirmBtn.addEventListener("click", async () => {
        const user = input.value.trim();
        if (!user) {
            errorOut.textContent = "Please input a username.";
            input.focus();
            return;
        }
        try {
            await assignUserToProject(user);
            modal.close();
        } catch (err) {
            errorOut.textContent = err.message;
        }
    });
});
