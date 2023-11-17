//import { Player, RemotePlayer } from "./Player";


dummy_token = "1234567890";



const socket = new WebSocket('ws://localhost:8080');

req = new UserRequest(socket, dummy_token);


function send_ball(that_room, x, y)
{
    var type="user";
    var command = "BALL";
    var room = that_room;
    var args = {posX: ball.x, posY: ball.y, room: that_room}
    var data = {type: type, command: command, args: args};
    socket.send(JSON.stringify(data));
}


function send_player(that_room, x, y)
{
    var type="user";
    var command = "MOVE";
    var room = that_room;
    var args = {posX: p1.x, posY: p1.y, room: that_room}
    var data = {type: type, command: command, args: args};
    socket.send(JSON.stringify(data));
}

function send_join(that_room, that_password)
{
    req.request("JOIN", {name: that_room, password: that_password});
}

function send_get_what(what_type, that_room)
{
    var type="user";
    var command = "GET";
    var what = what_type;
    var args = {room: that_room, what: what}
    var data = {type: type, command: command, args: args};
    socket.send(JSON.stringify(data));
}

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

function create_room()
{
    var password = document.getElementById("password").value;
    var room = document.getElementById("roomName").value;
    console.log("Creating room: " + room + " with password: " + password);
    var type="admin";
    var command = "CRTROOM";
    var args = {name: room, password: password}
    var data = {command: command, password: password, args: args};
    var data_fixed = {type: type, data: data};
    socket.send(JSON.stringify(data_fixed));
}


function join_room()
{
    var room = document.getElementById("roomName").value;
    var password = document.getElementById("password").value;
    send_join(room, password);
    console.log("Joining room: " + room + " with password: " + password);
}




