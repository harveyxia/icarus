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
            pointStart: Date.UTC(2014, 09, 08),
            data: null,
            visible: false,
            showInLegend: false
        }]
}

function drawViz(data) {

    if (data) {
        chart.series.push({
            name: data.name,
            pointInterval: 24 * 3600 * 1000,
            pointStart: Date.UTC(2014, 09, 08),
            data: data.data,
            color: 'rgba(124, 181, 236, 1)',
            fillColor: 'rgba(124, 181, 236, 0.2)'
        });
    }
    
    $('#viz').highcharts(chart);
}

$(document).ready(function() {
    var name = '{{ name }}';
    pollTimer = null;

    function initData(name) {
        $.ajax({
            url: '/data/' + name + '.json',
            success: function(data) {
                console.log(data);
                clearInterval(pollTimer);
                drawViz(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
                setTimeout(function() {
                    // use global var to clear timer
                    pollTimer = setInterval(function() {
                        pollData(name)
                    }, 5000);
                }, 30000);
            }
        });
    }

    function pollData(name) {
        $.ajax({
            url: '/data/' + name + '.json',
            success: function(data) {
                console.log(data);
                clearInterval(pollTimer);
                drawViz(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    }

    $('#add-flight').click(function() {
        var f = $("input[name='origin']").val();
        var t = $("input[name='destination']").val();
        var days = $("input[name='days']").val();
        $.ajax({
            url: '/scrape?f=' + f + '&t=' + t + '&days=' + days,
            success: function(data) {
                console.log(data);
                drawViz(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    });
    
    // draw empty graph
    drawViz();
});