//import { Player, RemotePlayer } from "./Player";
import Pong from "./Game.js";


var dummy_token = "1234567890";

const socket = new WebSocket('ws://localhost:8765');
var idofplayer = document.getElementById("id");
var button = document.getElementById("joingame");
var game;

button.addEventListener("click", function(){
    console.log("button clicked");
    var canvas = document.getElementById("canvas_game");
    game = new Pong(dummy_token, canvas, socket, idofplayer.value);
});
socket.onopen = function(e) {
    console.log("[open] Connection established");
};


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


