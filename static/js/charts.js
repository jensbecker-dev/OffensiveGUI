document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("targetsPieChart");

    if (canvas) {
        const ctx = canvas.getContext("2d");
        const totalTargets = parseInt(canvas.dataset.totalTargets, 10) || 0;
        const onlineTargets = parseInt(canvas.dataset.onlineTargets, 10) || 0;
        const offlineTargets = totalTargets - onlineTargets;

        new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["Online Targets", "Offline Targets"],
                datasets: [
                    {
                        data: [onlineTargets, offlineTargets],
                        backgroundColor: ["#29B6F6", "#FF7043"],
                        hoverBackgroundColor: ["#0288D1", "#F4511E"],
                        borderColor: ["#ffffff", "#ffffff"],
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom",
                    },
                },
            },
        });
    }
});
