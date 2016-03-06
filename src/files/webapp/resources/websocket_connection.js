var gatewaySocket = null;
var isGatewaySocketOpen = false;

$(window).load(function() {

    if (window.location.protocol === "https:")
    {
        gatewaySocket = new WebSocket(serverAdressSecure);
    }
    else
    {
        gatewaySocket = new WebSocket(serverAdress);
    }

    gatewaySocket.onopen = function()
    {
        console.log("Connection opened.");
        isGatewaySocketOpen = true;
    }

    gatewaySocket.onmessage = function(e)
    {
        response = e.data
        console.log("Message received: " + response);

        if (typeof response == "string")
        {
            // if (response == "OK")
            // {

            // }
            // else
            // {
            //     alert("Fehler aufgetreten: " + response)
            // }
        }
    }

    gatewaySocket.onclose = function(e)
    {
        console.log("Connection closed.");

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
