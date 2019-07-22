function pieChart(elementId,the_title,the_series){
    
    Highcharts.chart(elementId, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: the_title
        },
        tooltip: {
            // pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            pointFormat: '<b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    // format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    format: '{point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                },
                    showInLegend: true
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -100,
            y: 100,
            floating: true,
            borderWidth: 1,
            backgroundColor: '#FFFFFF',
            shadow: true
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
        series: the_series,
        
    });

}

