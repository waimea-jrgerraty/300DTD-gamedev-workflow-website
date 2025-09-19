document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('profile-container');
    const userid = container.dataset.userid;

    const roleSelect = document.getElementById('role-select');
    roleSelect?.addEventListener('change', async () => {
        const newRole = roleSelect.value;
        console.log("AAAH", newRole);
        try {
            const res = await fetch(`/api/user/${userid}/role`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ role: newRole })
            });
            if (res.ok) {
                document.getElementById('current-role').textContent = newRole;
                // alert('Role updated successfully!');
            } else {
                alert('Failed to update role.');
            }
        } catch (err) {
            console.error(err);
            alert('Error updating role.');
        }
    });

    // Avatar change
    const avatarInput = document.getElementById('avatar-input');
    const avatarBtn = document.getElementById('avatar-btn');

    avatarBtn?.addEventListener('click', async () => {
        if (!avatarInput.files.length) return alert('Select an image first.');
        const formData = new FormData();
        formData.append('avatar', avatarInput.files[0]);

        try {
            const res = await fetch(`/api/user/${userid}/avatar`, {
                method: 'PATCH',
                body: formData
            });
            if (res.ok) {
                // Add cache buster to reload images
                const timestamp = new Date().getTime();

                // Update profile avatar
                const profileAvatar = document.getElementById('profile-avatar');
                profileAvatar.src = `/user/${userid}/icon?${timestamp}`;

                // Update nav user icon
                const navIcon = document.getElementById('nav-user-icon');
                if (navIcon) {
                    navIcon.src = `/user/${userid}/icon?${timestamp}`;
                }
            } else {
                alert('Failed to update avatar.');
            }
        } catch (err) {
            console.error(err);
            alert('Error updating avatar.');
        }
    });
})