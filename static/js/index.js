// This file contains JavaScript code for the Nmap web application

document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript loaded successfully!");

    // Handle form submission for the Nmap scan
    const nmapForm = document.querySelector("form");
    if (nmapForm) {
        nmapForm.addEventListener("submit", (event) => {
            event.preventDefault(); // Prevent default form submission

            // Show a loading message with animation
            let loadingMessage = document.querySelector("#loading-message");
            if (!loadingMessage) {
                loadingMessage = document.createElement("div");
                loadingMessage.id = "loading-message";
                loadingMessage.textContent = "Running Nmap scan, please wait...";
                loadingMessage.style.color = "blue";
                loadingMessage.style.marginTop = "10px";
                loadingMessage.style.fontSize = "16px";
                loadingMessage.style.fontWeight = "bold";
                loadingMessage.style.animation = "fadeIn 1s ease-in-out infinite";
                nmapForm.appendChild(loadingMessage);
            }

            // Disable the submit button to prevent multiple submissions
            const submitButton = nmapForm.querySelector("button[type='submit']");
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.style.opacity = "0.6";
                submitButton.textContent = "Scanning...";
            }

            // Simulate a delay for the scan process (e.g., 5 seconds)
            setTimeout(() => {
                // Remove the loading message
                if (loadingMessage) {
                    loadingMessage.remove();
                }

                // Re-enable the submit button
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.style.opacity = "1";
                    submitButton.textContent = "Submit";
                }

                // Show a success message
                const successMessage = document.createElement("div");
                successMessage.id = "success-message";
                successMessage.textContent = "Nmap scan completed successfully!";
                successMessage.style.color = "green";
                successMessage.style.marginTop = "10px";
                successMessage.style.fontSize = "16px";
                successMessage.style.fontWeight = "bold";
                successMessage.style.animation = "fadeIn 1s ease-in-out";
                nmapForm.appendChild(successMessage);

                // Automatically remove the success message after 5 seconds
                setTimeout(() => {
                    if (successMessage) {
                        successMessage.remove();
                    }
                }, 5000);
            }, 5000);
        });
    }

    // Add a hover effect to the submit button
    const submitButton = nmapForm?.querySelector("button[type='submit']");
    if (submitButton) {
        submitButton.addEventListener("mouseover", () => {
            submitButton.style.backgroundColor = "#4CAF50";
            submitButton.style.color = "white";
            submitButton.style.transition = "background-color 0.3s ease";
        });

        submitButton.addEventListener("mouseout", () => {
            submitButton.style.backgroundColor = "";
            submitButton.style.color = "";
        });
    }
});

// Add CSS animations dynamically
const style = document.createElement("style");
style.textContent = `
    @keyframes fadeIn {
        0% { opacity: 0; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
`;
document.head.appendChild(style);