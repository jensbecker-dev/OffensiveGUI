document.addEventListener("DOMContentLoaded", function () {
    const sidebarItems = document.querySelectorAll(".sidebar ul li");

    sidebarItems.forEach((item) => {
        item.addEventListener("mouseenter", () => {
            item.style.backgroundColor = "#007bff";
            item.style.color = "white";
            item.style.transform = "scale(1.05)";
        });

        item.addEventListener("mouseleave", () => {
            item.style.backgroundColor = "";
            item.style.color = "";
            item.style.transform = "";
        });
    });
});