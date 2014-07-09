$(function() {
    $('#container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'BOS to HNL'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Price'
            }
        },
        series: [{
            type: 'area',
            name: 'BOS to HNL',
            pointInterval: 24 * 3600 * 1000,
            pointStart: Date.UTC(2014, 9, 8),
            data: [
            ]
        }]
    });
});