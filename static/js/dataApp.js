$(document).ready(function () {
    var x = data[0]
    var humidity = data[1]
    var temperature = data[2]
    var trace1;
    var trace2;
	var layout;

    trace1 = {
        x: x,
        y: temperature,
        name: "Temperature"
    };
    trace2 = {
        x: x,
        y: humidity,
        name: "Humidity"
    };
    layout = {
        title: 'Data',
        xaxis: {
            title: 'X',
        },
        yaxis: {
            title: 'Y',
        }
    };
    var traces = new Array();
    traces.push(trace1, trace2);
    Plotly.newPlot($('#plotdiv')[0], traces, layout);
})

