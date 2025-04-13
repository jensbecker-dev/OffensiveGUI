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
                        backgroundColor: ["#29B6F6", "#305b66"],
                        hoverBackgroundColor: ["#2aff00", "#ff4040"],
                        borderColor: ["#FFFFFF", "#FFFFFF"],
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
