/* PLOT 1 *************************************************************************************/
function chartOEE(valors) {

    const ctx = document.getElementById('myChart');
    const background_color = ['#33a3ec', '#ffce55', '#4ac1c1', '#ff00ff00'];

    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Availability', 'Performance', 'Quality'],
            datasets: [{
                data: valors,
                backgroundColor: background_color,
                borderWidth: 10,
                borderColor: "#fbfbfb"
            }]
        },
        options: {
            scales: {
                display: false
            },
            animation: {
                duration: 1000,
                animateRotate: true,
                render: false
            },
            plugins: {
                title: {
                    display: true,
                    text: "Pieces fabricated"
                },
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        },
        plugins: [ChartDataLabels],
        options: {
            plugins: {
                datalabels: {
                    color: ['black', 'black', 'black', 'white'],
                    font: { weight: 'bold', size: '14px' }
                }
            }
        }
    });
}

/* PLOT 2 *************************************************************************************/
function chartOkNok(valors) {

    const ctx2 = document.getElementById('myChart2');
    const background_color2 = ['#33a3ec', '#ff6384'];

    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Ok', 'No Ok'],
            datasets: [{
                data: valors,
                backgroundColor: background_color2,
                borderWidth: 10,
                borderColor: "#fbfbfb"
            }]
        },
        options: {
            scales: {
                display: false
            },
            animation: {
                duration: 1000,
                animateRotate: true,
                render: false
            },
            plugins: {
                title: {
                    display: true,
                    text: "Pieces fabricated"
                },
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        },
        plugins: [ChartDataLabels],
        options: {
            plugins: {
                datalabels: {
                    color: 'black',
                    font: { weight: 'bold', size: '14px' }
                }
            }
        }
    });
}

/* PLOT 3 *************************************************************************************/
function chartMachinesStatus(valors) {

    const ctx3 = document.getElementById('myChart3');
    const background_color3 = ['#33a3ec', '#ffce55', '#4ac1c1', '#ff6384'];

    new Chart(ctx3, {
        type: 'doughnut',
        data: {
            labels: ['Auto', 'Break', 'Stopped machine', 'Error'],
            datasets: [{
                data: valors,
                backgroundColor: background_color3,
                borderWidth: 10,
                borderColor: "#fbfbfb"
            }]
        },
        options: {
            scales: {
                display: false
            },
            animation: {
                duration: 1000,
                animateRotate: true,
                render: false
            },
            plugins: {
                title: {
                    display: true,
                    text: "Time distribution"
                },
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        },
        plugins: [ChartDataLabels],
        options: {
            plugins: {
                datalabels: {
                    color: 'black',
                    font: { weight: 'bold', size: '14px' }
                }
            }
        }
    });
}

/* PLOT 4 *************************************************************************************/
function chart4plot(valors) {

    const ctx4 = document.getElementById('myChart4');
    const background_color4 = ['#33a3ec', '#ffce55', '#4ac1c1', '#9966ff'];

    new Chart(ctx4, {

        type: 'bar',
        data: {
            labels: ['OEE', 'Availability', 'Performance', 'Quality'],
            datasets: [{
                data: valors,
                backgroundColor: background_color4,
                borderColor: "#fbfbfb",
                borderWidth: -1,
                maxBarThickness: 40
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false } },
                y: { grid: { display: false } }
            },
            indexAxis: 'y',
            animation: {
                duration: 1000,
                animateRotate: true,
                render: false
            },
            plugins: {
                legend: {
                    display: false,
                }
            }
        },
        plugins: [ChartDataLabels],
        options: {
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false } },
                y: { grid: { display: false } }
            },
            animation: {
                duration: 1000,
                animateRotate: true,
                render: false
            },
            plugins: {
                legend: {
                    display: false,
                }
            },
            indexAxis: 'y',
            plugins: {
                datalabels: {
                    color: 'black',
                    font: { weight: 'bold', size: '14px' }
                }
            }
        }
    });
}