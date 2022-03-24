ChartScriptHead="""Highcharts.chart('ossechart', {

exporting: {
        buttons: {
            contextButton: {
                enabled: false
            }    
        }
    },

boost: {
        useGPUTranslations: true,
        // Chart-level boost when there are more than 5 series in the chart
        seriesThreshold: 1
    },


  chart: {
        backgroundColor: 'rgba(0,0,0,0)',
        zoomType: 'xy',
        type: 'line',
        height: 270
    },


title: {
        text: ''
    },

    yAxis: {
        title: {
            text: 'Alerts Numbers'
        }
    },

       xAxis: {
            type: 'datetime',
            },

    legend: {
        layout: 'horizontal',
        align: 'center',
        verticalAlign: 'bottom'
    },


    series: [{
       boostThreshold: 1,
"""



ChartScriptTail="""    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
			enabled: true,
                }
            }
        }]
    }

});

"""
