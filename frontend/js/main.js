//import { Player, RemotePlayer } from "./Player";
import UserRequest  from "./Request.js";

var dummy_token = "1234567890";



const socket = new WebSocket('ws://localhost:8080');

var req = new UserRequest(socket, dummy_token);


socket.onopen = function(e) {
    console.log("[open] Connection established");

};

socket.onmessage = eachRecieve;

function eachRecieve(event)
{
    data = JSON.parse(event.data);
    console.log(data);
}

socket.onclose = function(event) {

    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {

        console.log('[close] Connection died');
    }
};

socket.onerror = function(error) {
    console.log(`[error] ${error.message}`);
}

function update_token()
{
    var token = document.getElementById("token").value;
    req.set_token(token);
}


