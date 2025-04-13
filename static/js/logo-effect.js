document.addEventListener("DOMContentLoaded", () => {
    const logo = document.querySelector(".logo-container");

    if (logo) {
        let hue = 0;

        // Pulsating effect for border and logo
        setInterval(() => {
            hue = (hue + 1) % 360;
            const color = `rgba(0, 204, 255, 1)`; // Updated color
            logo.style.border = `5px solid ${color}`;
            logo.style.boxShadow = `0 0 15px ${color}, 0 0 30px ${color}`;
            logo.style.background = `rgba(0, 0, 0, 0)`; // Removed extra parenthesis
            logo.style.backgroundClip = "text";
            logo.style.webkitBackgroundClip = "text";
            logo.style.webkitTextFillColor = "transparent";
        }, 50);

        // Enhanced glitch effect
        setInterval(() => {
            if (Math.random() < 0.5) { // 50% chance to trigger the glitch
                const glitchLayer = document.createElement("div");
                glitchLayer.classList.add("glitch-layer");
                glitchLayer.style.position = "absolute";
                glitchLayer.style.top = `${Math.random() * 100}%`;
                glitchLayer.style.left = `${Math.random() * 100}%`;
                glitchLayer.style.width = `${Math.random() * 30 + 10}px`;
                glitchLayer.style.height = `${Math.random() * 10 + 5}px`;
                glitchLayer.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
                glitchLayer.style.clipPath = `polygon(0 0, 100% 0, 100% 100%, 0 100%)`;
                glitchLayer.style.transform = `translate(${Math.random() * 10 - 5}px, ${Math.random() * 10 - 5}px)`;
                glitchLayer.style.zIndex = "10";
                glitchLayer.style.pointerEvents = "none";

                logo.appendChild(glitchLayer);

                setTimeout(() => {
                    logo.removeChild(glitchLayer);
                }, 100); // Glitch lasts for 100ms
            }
        }, 300); // Check for glitch every 300ms
    }
});
