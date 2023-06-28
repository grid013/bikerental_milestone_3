const xValues = ["Aug", "Sept", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"];
const yValues = [40, 50, 55, 60, 70, 80, 85, 88];

new Chart("myChart", {
    type: "line",
    data: {
        labels: xValues,
        datasets: [{
            fill: false,
            lineTension: 0.5,
            backgroundColor: "red",
            borderColor: "red",
            borderWidth: 3,
            pointRadius: 3.5,
            data: yValues
        }]
    },
    options: {
        legend: { display: false },
        scales: {
            yAxes: [{ ticks: { min: 0, max: 100 } }],
        },
        plugins: {
            title: {
                display: true,
                text: "% Bikes rented over last 8 months",
                font: { weight: 'bold', size: 20 },

            },
            legend: {
                display: false,
                position: 'bottom',
            },
        }
    }
});