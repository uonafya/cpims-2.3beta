function stackedBar(elementId,titlee,categoriee,serie,stackType,legend){
    Highcharts.chart(elementId, {
        chart: {
            type: 'column'
        },
        title: {
            text: titlee
        },
        xAxis: {
            categories: categoriee
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Count'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            layout: legend.layout,
            align: 'right',
            x: legend.x,
            verticalAlign: legend.verticalAlign,
            y: legend.y,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: stackType,
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        colors: [
                '#F2784B',
                '#1BA39C',
                '#913D88',
                '#4d79ff',
                '#80ff00',
                '#ff8000',
                '#00ffff',
                '#ff4000'
            ],
        series: serie

    });

}

