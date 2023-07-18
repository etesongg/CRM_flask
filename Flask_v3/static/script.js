const Age_chart = document.getElementById('AgeGroup_Chart');
const Mon_chart = document.getElementById('MonthlySales_Chart');
    

function Bar_Chart() {
    new Chart(Age_chart, {
        type: 'bar',
        data: {
        labels: labels ,
        datasets: [
            {
            data: data ,
        backgroundColor: [
            'rgb(29, 91, 121)',
            'rgb(70, 139, 151)',
            'rgb(239, 98, 98)',
            'rgb(243, 170, 96)',
            'rgb(74, 85, 162)',
            'rgb(255, 102, 102)'
            ]
        }]
        },
        options: {
            plugins:{
                legend:{
                    display:false
                },
            }
        }
    });
}
Bar_Chart()

function mixed_Chart() {
    new Chart(Mon_chart, {
        data: {
            datasets: [{
                type: 'bar',
                label: 'TotalRevenue',
                data: data,
                borderColor: 'rgb(58, 166, 185)',
                backgroundColor: 'rgba(58, 166, 185 ,0.4)',
                yAxisID: 'y1'
            }, {
                type: 'line',
                label: 'ItemCount',
                data: data2,
                borderColor: 'rgb(255, 158, 170)',
                backgroundColor: 'rgba(255, 158, 170,0.2)',
                yAxisID: 'y2'
            }],
            labels: labels
        },
        options: {
            scales: {
                y1: {
                    position: 'left',
                    ticks: {
                        callback: function(value, index, ticks) {
                            return `${value.toLocaleString()}원`;
                        }
                    }
                },
                y2: {
                    beginAtZero: true,
                    position: 'right',
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        stepSize:1,
                        callback: function(value, index, ticks) {
                            return `${value.toLocaleString()}개`;
                        }
                    }
                }
            }
        }
    });
}
mixed_Chart()
    