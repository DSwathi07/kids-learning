document.addEventListener('DOMContentLoaded', () => {
    // Handle profile picture preview
    const profilePicInput = document.querySelector('#profile_pic');
    if (profilePicInput) {
        profilePicInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const img = document.querySelector('img[alt="Profile Picture"]');
                    img.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});