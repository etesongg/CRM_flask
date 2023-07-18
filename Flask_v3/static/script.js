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
                data: data
            }, {
                type: 'line',
                label: 'ItemCount',
                data: data2,
            }],
            labels: labels
        }

    });
}
mixed_Chart()
    