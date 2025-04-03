document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript loaded successfully!");

    // Handle form submission for the Nmap scan
    const nmapForm = document.querySelector("form");
    if (nmapForm) {
        nmapForm.addEventListener("submit", (event) => {
            // Show a loading message or spinner
            const loadingMessage = document.createElement("div");
            loadingMessage.id = "loading-message";
            loadingMessage.textContent = "Running Nmap scan, please wait...";
            loadingMessage.style.color = "blue";
            loadingMessage.style.marginTop = "10px";
            nmapForm.appendChild(loadingMessage);

            // Disable the submit button to prevent multiple submissions
            const submitButton = nmapForm.querySelector("button[type='submit']");
            if (submitButton) {
                submitButton.disabled = true;
            }
        });
    }
});