function processData(data) {
    var processedData = [];
    for (item in data) {
        // console.log(Date.parse());
        processedData.push([Number(Date.parse(item)), Number(data[item].replace(/[^0-9]/g,''))]);
    }
    console.log(processedData);
    processedData.sort(function(a, b) {
        return a[0] - b[0];
    });
    return processedData;
}

var processedData = processData(data);

$(function() {
    var chart = {
        chart: {
            type: 'line'
        },
        credits: {
            enabled: false
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
            data: processedData
        }]
    }
    $('#container').highcharts(chart);
});