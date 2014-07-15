function drawViz(data) {
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
            title: {
                text: 'Flights',
                style: { fontWeight: 'bold', fontSize: '16px' }
            }
        },
        yAxis: {
            title: {
                text: 'Price',
                style: { fontWeight: 'bold', fontSize: '16px' }
            },
            labels: {
                formatter: function() { return '$' + this.value; }
            }
        },
        tooltip: {
            valuePrefix: '$',
            shared: true
            // formatter: function() {
            //     var date = new Date(Date(this.x));
            //     var dateStr = ''
            //     var tooltip = '<b>' + this.series.name + '</b><br/>' +
            //                     date + ' ' + this.y
            //     return tooltip
            // }
            // pointFormat: function() { return this.value }
        },
        plotOptions: {
        },
        series: [{
            name: data.name,
            pointInterval: 24 * 3600 * 1000,
            pointStart: Date.UTC(2014, 09, 08),
            data: data.data,
            color: 'rgba(124, 181, 236, 1)',
            fillColor: 'rgba(124, 181, 236, 0.2)'
        }]
    }
    $('#container').highcharts(chart);
}