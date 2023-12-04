import {Player, Ball} from "./Player.js";
import Request from "./Request.js";



class Game{
	constructor(canvas, url)
	{
		this.canvas = canvas;
		this.ctx = canvas.getContext("2d");
		this.url = url;
	}


	join_game(gameid, gamepass, player, playerpass)
	{
		var req = new Request(this.url);
		var url = "/join_game";
		var data = {gameid: gameid, password: gamepass, player: player, player_pass: playerpass};
		req.post(url, data).then(function(response){
			return response.json();
		}).then(function(data){
			console.log(data);
		}).catch(function(error){
			console.log(error);
		});
	}

	game_info(gameid)
	{
		var req = new Request(this.url);
		var url = "/info/" + gameid;
		var data = null;
		data = req.get(url).then(function(response){
			return response.json();
		}).then(function(data){
			return data;
		});
		return data;
	}

	move(gameid, gamepass, player, playerpass, direction)
	{
		var req = new Request(this.url);
		var url = "/move";
		var data = {gameid: gameid, password: gamepass, player: player, player_pass: playerpass, direction: direction};
		return req.post(url, data).then(function(response){
			return response.json();
		}).then(function(data){
			return data;
		}).catch(function(error){
			console.log(error);
		});
	}

};