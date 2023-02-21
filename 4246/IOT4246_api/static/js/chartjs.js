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
        }, options: {
            scales: {
                display: false
            },
            animation: {
                duration: 1000,
                animateRotate: true,
                render: false
            },
            plugins: {
                datalabels: {
                    display: true,
                    align: 'bottom',
                    backgroundColor: '#ccc',
                    borderRadius: 3,
                    font: {
                        size: 18,
                    },
                },
                title: {
                    display: true,
                    text: "Pieces fabricated"
                },
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });
}

/* PLOT 2 *************************************************************************************/
const ctx2 = document.getElementById('myChart2');
const background_color2 = ['#33a3ec', '#ff6384'];

function chartOkNok(valors) {
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
        }
    });
}

/* PLOT 3 *************************************************************************************/
const ctx3 = document.getElementById('myChart3');
const background_color3 = ['#33a3ec', '#ffce55', '#4ac1c1', '#ff6384'];

function chartMachinesStatus(valors) {
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
        }
    });
}

/* PLOT 4 *************************************************************************************/
const ctx4 = document.getElementById('myChart4');
const background_color4 = ['#33a3ec', '#ffce55', '#4ac1c1', '#ff6384'];

function chart4plot(valors) {
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
            
            indexAxis: 'y',
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display: false
                    }
                }]
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
            }
        }
    }); 
}