$(document).ready(function () {
  namespace = '/main';
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  socket.on('connect', function() {
    socket.emit('message_event', {data: 'I\'m connected!'});
  });

  socket.on('message_response', function(msg) {
    $('#log').append('Received #' + msg.message + '<br>').html();
  });

  $('form#open').submit(function (event) {
    socket.emit('open_request');
    return false;
  });

  $('form#disconnect').submit(function (event) {
      socket.emit('disconnect_request');
      return false;
  });
});