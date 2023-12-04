//import { Player, RemotePlayer } from "./Player";

import Request from "./Request.js";
import Game from "./Game.js";

var backendurl = "http://localhost:5000";
var endpoint = "/api"


var req = new Request(backendurl + endpoint);
var player = document.getElementById("player");
var gameid = document.getElementById("gameid");
var gamepass = document.getElementById("gamepass");
var playerpass = document.getElementById("playerpass");
var joinbutton = document.getElementById("joinbutton");
var gameinfo_button = document.getElementById("gameinfo_button");
var canvas = document.getElementById("canvas");

var game = new Game(canvas, backendurl + endpoint);


joinbutton.addEventListener("click", function(){

    var integer_val = parseInt(player.value);
    game.join_game(gameid.value, gamepass.value, integer_val, playerpass.value).then(function(data){

        console.log(data);
        game.set_parameters(gameid.value, gamepass.value, integer_val, playerpass.value);
            
    });
 
});


gameinfo_button.addEventListener("click", function()
{
    game.game_info(gameid.value).then(function(data){

        console.log(data);
    });
});



