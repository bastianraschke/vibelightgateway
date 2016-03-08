var gatewaySocket = null;
var isGatewaySocketOpen = false;

$(window).load(function() {

    var currentHost = window.location.host;

    if ( window.location.protocol == 'https:' )
    {
        var serverAdress = 'wss://' + currentHost + '/websocket/';
    }
    else
    {
        var serverAdress = 'ws://' + currentHost + '/websocket/';
    }

    gatewaySocket = new WebSocket(serverAdress);

    gatewaySocket.onopen = function()
    {
        console.log('Connection opened.');
        isGatewaySocketOpen = true;
    }

    gatewaySocket.onmessage = function(event)
    {
        response = event.data
        console.log('Message received: ' + response);

        /*
        if (typeof response == 'string')
        {
            if (response != 'OK')
            {
                alert('Fehler aufgetreten: ' + response)
            }
        }
        */
    }

    gatewaySocket.onclose = function(event)
    {
        console.log('Connection closed.');

        gatewaySocket = null;
        isGatewaySocketOpen = false;
    }

});

function sendWebsocketMessage(message)
{
    if (isGatewaySocketOpen)
    {
       gatewaySocket.send(message);
       return true;           
    }

    return false; 
};
