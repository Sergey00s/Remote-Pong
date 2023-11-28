//import { Player, RemotePlayer } from "./Player";
import Pong from "./Graphics.js";


var dummy_token = "1234567890";

const socket = new WebSocket('ws://localhost:2734');




var game = new Pong(document.getElementById("gameCanvas"), 800, 800, socket, dummy_token);

var roomname = document.getElementById("roomname");
var usertoken = document.getElementById("token");
var username = document.getElementById("username");
var userid = document.getElementById("userid");
var join_room_button = document.getElementById("joinroom");
var create_room_button = document.getElementById("createroom");


var game = new Pong(document.getElementById("gameCanvas"), 800, 800, socket, usertoken, username, userid, roomname);

join_room_button.addEventListener("click", join_room);
create_room_button.addEventListener("click", create_room);

function create_room()
{
    game.req.userid = userid.value;
    game.req.username = username.value;
    game.req.set_token(usertoken.value);
    game.req.send_room_command(roomname.value, "createroom");
}


function join_room()
{
    game.req.userid = userid.value;
    game.req.username = username.value;
    game.req.set_token(usertoken.value);
    game.req.send_room_command(roomname.value, "joinroom");
}


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


