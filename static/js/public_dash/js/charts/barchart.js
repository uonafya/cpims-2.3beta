function barChart(elementId,the_title,the_x_axis,the_series){
    console.log('barchart summoned');
    console.log('elementId: '+elementId);
    console.log('the_title: '+the_title);
    console.log('the_x_axis: '+the_x_axis);
    console.log('the_series: '+JSON.stringify(the_series));

    Highcharts.Chart({
        chart: {
            renderTo: elementId,
            type: 'column'
        },
        title: {
            text: the_title
        },
        xAxis: {
            categories: the_x_axis,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            // formatter: function() {
            //     return ''+ this.series.name +': '+ this.y +' millions';
            // }
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
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
        credits: {
            enabled: false
        },
        series: the_series
    });
    

}

