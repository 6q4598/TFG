// For CHART.JS plugins:

/***********************************
 * OEE CHART                       *
 ***********************************/
const ctx_oee = document.getElementById('myChart');
const background_color = ['#33a3ec', '#ffce55', '#4ac1c1', '#ff00ff00'];
// Chart.register(ChartDataLabels);

var chart_oee = new Chart(ctx_oee, {
    type: 'doughnut',
    data: {
        labels: ['Availability', 'Performance', 'Quality'],
        datasets: [{
            data: [0, 0, 0],
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
                text: "Current shift OEE"
            },
            legend: {
                display: true,
                position: 'bottom'
            }
        }
    },
    /*
    plugins: [ChartDataLabels],
    options: {
        plugins: {
            datalabels: {
                color: ['black', 'black', 'black', 'white'],
                font: { weight: 'bold', size: '14px' }
            }
        }
    }
    */
});

// Función para actualizar el gráfico con los valores de los sensores
function updateChartOee() {
    $.get('/oee', function(data) {
        console.log(data);
        chart_oee.data.datasets[0].data[0] = data.availability;
        chart_oee.data.datasets[0].data[1] = data.performance;
        chart_oee.data.datasets[0].data[2] = data.quality;
        chart_oee.update();
    });
}

// Actualizar el gráfico cada 5 segundos
setInterval(updateChartOee, 5000);

/***********************************
 * PIECES CHART                    *
 ***********************************/
var ctx_pieces = document.getElementById('myChart2').getContext('2d');
const background_color2 = ['#33a3ec', '#ff6384'];
// Chart.register(ChartDataLabels);

var chart_pieces = new Chart(ctx_pieces, {
    type: 'doughnut',
    data: {
        labels: ['OK', 'NOK'],
        datasets: [{
            data: [0, 0],
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
    /*
    plugins: [ChartDataLabels],
    options: {
        plugins: {
            datalabels: {
                color: ['black'],
                font: { weight: 'bold', size: '14px' }
            }
        }
    }
    */
});

// Función para actualizar el gráfico con los valores de los sensores
function updateChartPieces() {
    $.get('/pieces', function(data) {
        console.log("Data 2: ", data);
        chart_pieces.data.datasets[0].data[1] = data.pieces_nok;
        chart_pieces.data.datasets[0].data[0] = data.pieces_ok;
        chart_pieces.update();
    });
}

// Actualizar el gráfico cada 5 segundos
setInterval(updateChartPieces, 5000);




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
