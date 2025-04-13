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
                        backgroundColor: ["rgb(0, 155, 103)", "#ff3a00"],
                        hoverBackgroundColor: ["#2e8b57", "#ff4040"],
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
