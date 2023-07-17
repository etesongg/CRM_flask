const ctx = document.getElementById('revenue_Chart');
    

function Bar_Chart() {
    new Chart(ctx, {
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
    