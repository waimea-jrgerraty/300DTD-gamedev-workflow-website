document.getElementById("task-description").addEventListener("blur", async function () {
    const taskId = this.dataset.taskId;
    const description = this.value;

    const response = await fetch(`/api/update-description/${taskId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ description })
    });

    if (!response.ok) {
        console.error("Failed to update");
    }
});