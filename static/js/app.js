$(function () {
	$("#tabs").tabs({
		event: "mouseover"
	});
});
$(document).ready(function () {
	var x = new Array();
	var temperature = new Array();
	var humidity = new Array();
	// var trace;
	var layout;
	namespace = '/test';
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

	socket.on('connect', function () {
		socket.emit('my_event', {data: 'I\'m connected!', value: 1});
	});

	socket.on('data_response', function(message){
		var jsonData = JSON.parse(message.data)
		var amplitude = jsonData.amplitude;
		console.log(jsonData);
		$('#dataLog').append('Data received #' + message.count + ': Temperature = ' + jsonData.temperature + ", Humidity = " + jsonData.humidity + '<br>').html();
		x.push(parseFloat(message.count));
		temperature.push(parseFloat(jsonData.temperature));
		humidity.push(parseFloat(jsonData.humidity))
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

		var temperatureData = [
			{
				domain: {x: [0, 1], y: [0, 1]},
				value: jtemperature,
				title: {text: "Temperature"},
				type: "indicator",
				mode: "gauge+number",
				delta: {reference: 400},
				gauge: {axis: {range: [-50 * amplitude, 50 * amplitude]}}
			}
		];
		layout = {width: 600, height: 400};
		Plotly.newPlot('temperatureDiv', temperatureData, layout);

		var humidityData = [
			{
				domain: {x: [0, 1], y: [0, 1]},
				value: humidity,
				title: {text: "Humidity"},
				type: "indicator",
				mode: "gauge+number",
				delta: {reference: 400},
				gauge: {axis: {range: [0, 100 * amplitude]}}
			}
		];
		layout = {width: 600, height: 400};
		Plotly.newPlot('humidityDiv', humidityData, layout);
	});

	socket.on('my_response', function (msg) {
		$('#log').append('Received #' + msg.count + ': ' + msg.data + '<br>').html();
	});

	$('form#emit').submit(function (event) {
		socket.emit('my_event', {value: $('#emit_value').val()});
		return false;
	});
	$('form#open').submit(function (event) {
		socket.emit('open', {data: 'Opened!', value: 2});
		return false;
	});
	$('form#disconnect').submit(function (event) {
		socket.emit('disconnect_request');
		return false;
	});
	$('#buttonVal').click(function (event) {
		console.log($('#buttonVal').val());
		socket.emit('click_event', {value: $('#buttonVal').val()});
		return false;
	});
	$('#start').click(function (event) {
		console.log($('#start').val());
		socket.emit('click_event', {value: $('#start').val()});
		return false;
	});
});