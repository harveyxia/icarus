var chart = {
    chart: {
        zoomType: 'x',
        type: 'area'
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Flight Prices'
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
        series: {
            marker: {
                enabled: false
            }
        }
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
            color: colorBrewer[seriesNum],
            fillColor: colorBrewer[seriesNum].substr(0, colorBrewer[seriesNum].length-4) + ',0.2)'
        });
    }
    console.log(colorBrewer[seriesNum].substr(0, colorBrewer[seriesNum].length-4) + ',0.2)');
    seriesNum += 1;
    $('#viz').highcharts(chart);
}

// 12 colors for different series
var colorBrewer = ["rgba(141,211,199, 1)",
                   "rgba(141,211,199, 1)","rgba(209,209,179, 1)","rgba(190,186,218, 1)",
                   "rgba(251,128,114, 1)","rgba(128,177,211, 1)","rgba(253,180,98, 1)",
                   "rgba(179,222,105, 1)","rgba(252,205,229, 1)","rgba(217,217,217, 1)",
                   "rgba(188,128,189, 1)","rgba(204,235,197, 1)","rgba(255,237,111, 1)"]
var seriesNum = 0;

$(document).ready(function() {
    // var name = '{{ name }}';
    // pollTimer = null;

    // function initData(name) {
    //     $.ajax({
    //         url: '/data/' + name + '.json',
    //         success: function(data) {
    //             console.log(data);
    //             clearInterval(pollTimer);
    //             drawViz(data);
    //         },
    //         error: function(jqXHR, textStatus, errorThrown) {
    //             console.log(errorThrown + ' Begin polling data');
    //             setTimeout(function() {
    //                 // use global var to clear timer
    //                 pollTimer = setInterval(function() {
    //                     pollData(name)
    //                 }, 5000);
    //             }, 30000);
    //         }
    //     });
    // }

    function pollData(name) {
        $.ajax({
            url: '/data/' + name + '.json',
            success: function(data) {
                console.log(data);
                clearInterval(pollTimer);
                $('#loading-bar').width(0);
                $('#loading-bar-container').slideUp();
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
                if (typeof data === 'object') {
                    drawViz(data);
                } else {
                    $('#loading-bar-container > span').text('scraping flight ' + f + ' to ' + t + ' for ' + days + ' days')
                    $('#loading-bar-container').slideDown();
                    $('#loading-bar').animate({width: '100%'}, 60000);
                    setTimeout(function() {
                        // use global var to clear timer
                        pollTimer = setInterval(function() {
                            pollData(data);
                        }, 5000);
                    }, 30000);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    });
    
    // draw empty graph
    drawViz();
});