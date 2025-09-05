document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.getElementById("open-add-user");
    const modal = document.getElementById("add-user-modal");
    const cancelBtn = document.getElementById("cancel-add-user");
    const confirmBtn = document.getElementById("confirm-add-user");
    const input = document.getElementById("member-input");
    const datalist = document.getElementById("project-members");
    const errorOut = document.getElementById("add-user-error");

    // Read IDs from dataset
    const TASK_ID = openBtn.dataset.taskId;
    const PROJECT_ID = openBtn.dataset.projectId;

    let memberIndex = new Map();

    async function loadMembers() {
        memberIndex.clear();
        datalist.innerHTML = "";

        const res = await fetch(`/api/project/${PROJECT_ID}/members`);
        if (!res.ok) throw new Error("Failed to load members");
        const members = await res.json();

        for (const m of members) {
            const label = m.name ? `${m.name} (${m.username})` : m.username;
            const opt = document.createElement("option");
            opt.label = label;
            opt.value = m.username;
            opt.dataset.userId = m.id;
            datalist.appendChild(opt);
            memberIndex.set(m.username, { id: m.id, username: m.username });
        }
    }

    function resolveSelectedUser() {
        const val = input.value.trim();
        if (memberIndex.has(val)) return memberIndex.get(val);
        for (const opt of datalist.options) {
            if (opt.label === val || opt.value === val) {
                return { id: parseInt(opt.dataset.userId, 10), username: opt.value };
            }
        }
        return null;
    }

    async function assignUserToTask(userId) {
        const res = await fetch(`/api/tasks/${TASK_ID}/assign`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId })
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
            await loadMembers();
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
        const user = resolveSelectedUser();
        if (!user) {
            errorOut.textContent = "Please select a user from the list.";
            input.focus();
            return;
        }
        try {
            await assignUserToTask(user.id);
            modal.close();
            // Optional: refresh UI
            // location.reload();
        } catch (err) {
            errorOut.textContent = err.message;
        }
    });
});
