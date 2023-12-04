//import { Player, RemotePlayer } from "./Player";

import Request from "./Request.js";


var backendurl = "http://localhost:5000";
var endpoint = "/api"


var req = new Request(backendurl + endpoint);
var player = document.getElementById("player");
var gameid = document.getElementById("gameid");
var gamepass = document.getElementById("gamepass");
var playerpass = document.getElementById("playerpass");
var joinbutton = document.getElementById("joinbutton");
var gameinfo_button = document.getElementById("gameinfo_button");



joinbutton.addEventListener("click", function(){

    var url = "/join_game";
    var data = {gameid: gameid.value, password: gamepass.value, player: player.value, player_pass: playerpass.value};
    req.post(url, data).then(function(response){
        return response.json();
    }).then(function(data){
        console.log(data);
    }).catch(function(error){
        console.log(error);
    });
});


gameinfo_button.addEventListener("click", function(){
    
        var url = "/info/" + gameid.value
        req.get(url).then(function(response){
            console.log(response.response);
        });
});



