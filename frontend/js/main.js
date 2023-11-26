//import { Player, RemotePlayer } from "./Player";
import Pong from "./Graphics.js";


var dummy_token = "1234567890";

const socket = new WebSocket('ws://localhost:2734');


var update_token_button = document.getElementById("update");
update_token_button.addEventListener("click", update_token);

var start_game_button = document.getElementById("start");
start_game_button.addEventListener("click", start_game);

var game = new Pong(document.getElementById("gameCanvas"), 800, 800, socket, dummy_token);




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

function update_token()
{
    var token = document.getElementById("token").value;
    game.req.set_token(token);
}


function start_game()
{
    var data = {type: "admin", data: {password: "admin", command: "CRTROOM", args: {name: "test", password: "admin"}}}; 
    socket.send(JSON.stringify(data));
    data = {type: "user", data: {user_token: game.req.token, command: "JOIN", args: {name: "test", password: "admin"}}};
    socket.send(JSON.stringify(data));
    game.run();
}
