document.addEventListener("DOMContentLoaded", () => {
    const logo = document.querySelector(".logo-container");

    if (logo) {
        let hue = 0;
        setInterval(() => {
            hue = (hue + 1) % 360;
            logo.style.border = `3px solid hsl(${hue}, 100%, 50%)`;
            logo.style.boxShadow = `0 0 15px hsl(${hue}, 100%, 50%), 0 0 30px hsl(${hue}, 100%, 50%)`;
            logo.style.transform = `scale(1.05)`;
        }, 50);
    }
});
