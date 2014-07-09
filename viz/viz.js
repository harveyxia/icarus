$(function() {
    var chart = {
        chart: {
            zoomType: 'x',
            type: 'area'
        },
        credits: {
            enabled: false
        },
        title: {
            text: 'BOS, Roundtrip, 10 Days'
        },
        xAxis: {
            type: 'datetime',
            // labels: {
            //     formatter: function()
            // }
        },
        yAxis: {
            title: {
                text: 'Price'
            }
        },
        plotOptions: {
            area: {
            //     fillColor: {
            //         linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
            //         stops: [
            //                     [0, Highcharts.getOptions().colors[0]],
            //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            //                 ]
            //     }
            }
        },
        series: [{
            name: 'BOS to HNL',
            pointInterval: 24 * 3600 * 1000,
            pointStart: Date.UTC(2014, 09, 08),
            data: data1,
            color: 'red',
            fillColor: 'rgba(255, 0, 0, 0.4)'
        }, {
            name: 'BOS to BCN',
            pointInterval: 24 * 3600 * 1000,
            pointStart: Date.UTC(2014, 09, 08),
            data: data2,
            color: 'rgba(124, 181, 236, 1)',
            fillColor: 'rgba(124, 181, 236, 0.4)'
        }]
    }
    $('#container').highcharts(chart);
});