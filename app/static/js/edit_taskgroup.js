document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".editable-group-name").forEach(el => {
        // Triggers when the element loses focus
        el.addEventListener("blur", async function (e) {
            const groupId = e.target.dataset.groupId;
            const newName = e.target.value.trim();
            if (!groupId || !newName) return;

            // Send update request
            const res = await fetch(`/api/group/${groupId}/rename`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: newName })
            });

            if (!res.ok) {
                alert("Failed to rename group");
            }
        });

        // Optional: prevent Enter from creating a line break
        el.addEventListener("keydown", e => {
            if (e.key === "Enter") {
                e.preventDefault();
                e.target.blur();
            }
        });
    });

    // Also handle the new task_group button
    const addBtn = document.getElementById("addGroupBtn");

    addBtn.addEventListener("click", async (e) => {
        try {
            const projectId = addBtn.dataset.projectId;
            const categoryId = addBtn.dataset.categoryId;
            const res = await fetch(`/project/${projectId}/category/${categoryId}/group`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: "New Group" }) // default name
            });

            if (!res.ok) throw new Error("Failed to add group");

            location.reload(); // simplest approach
        } catch (err) {
            alert(err.message);
        }
    });

    // Also putting the fake <a> tag in here
    // This is needed so the task cards render properly (nesting <a> tags breaks everything)
    document.querySelectorAll(".user-icon-wrapper").forEach(el => {
        el.addEventListener("click", e => {
            e.stopPropagation();     // Prevent outer <a> click
            e.preventDefault();      // Prevent default browser action
            
            const userId = el.dataset.userId;
            window.location.href = `/user/${userId}/profile`;
        });
    });

});
