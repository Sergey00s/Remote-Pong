import {Player, Ball} from "./Player.js";
import Request from "./Request.js";



class Game{
	constructor(canvas, url)
	{
		this.canvas = canvas;
		this.ctx = canvas.getContext("2d");
		this.url = url;
		this.parameters = {gameid: null, gamepass: null, player: null, playerpass: null};
		this.score = {p1: 0, p2: 0};
		this.state = "waiting"
		this.ball = {x: -250, y: -250};
		this.owner_is = null;
		this.p1 = {x:-250, y:-250};
		this.p2 = {x:-250, y:-250};
		this.worldwidth = 1000;
		this.worldheight = 1000;
		this._checked = true;
		this.interval = null;
		document.addEventListener("keydown", this.keydown.bind(this));

		window.requestAnimationFrame(this.run.bind(this));
	}

	keydown(e)
	{
		if (this.owner_is != null && this.state != "gameover")
		{
			if (e.key == "w")
			{
				this.move(this.parameters.gameid, this.parameters.gamepass, this.parameters.player, this.parameters.playerpass, "up");
				console.log("w");
			}
			else if (e.key == "s")
			{
				console.log("s");
				this.move(this.parameters.gameid, this.parameters.gamepass, this.parameters.player, this.parameters.playerpass, "down");
			}
		}
	}

	update(data)
	{

			this.p1.x = data.p1_pos[0];
			this.p1.y = data.p1_pos[1];
			this.p2.x = data.p2_pos[0];
			this.p2.y = data.p2_pos[1];
			this.ball.x = data.ball_pos[0];
			this.ball.y = data.ball_pos[1];
			this.score.p1 = data.score1;
			this.score.p2 = data.score2;
			this.state = data.state;
	}

	info_update()
	{
		if (this.state != "gameover")
		{
			this.game_info(this.parameters.gameid).then(this.update.bind(this));
		}
	}

	run()
	{
		if (this._checked && this.parameters.gameid != null && this.parameters.gamepass != null && this.parameters.player != null && this.parameters.playerpass != null)
		{
			this.interval = setInterval(this.info_update.bind(this), 15);
			this._checked = false;
		}
		if (this.state == "gameover")
		{
			clearInterval(this.interval);
		}
		this.draw();		
		window.requestAnimationFrame(this.run.bind(this));
	}
	world_to_canvas(x, y)
	{
		var x = x / this.worldwidth * this.canvas.width;
		var y = y / this.worldheight * this.canvas.height;
		return {x: x, y: y};
	}

	draw_rect_by_canvas(x, y, w, h)
	{
		var x = x / this.worldwidth * this.canvas.width;
		var y = y / this.worldheight * this.canvas.height;
		var w = w / this.worldwidth * this.canvas.width;
		var h = h / this.worldheight * this.canvas.height;
		this.ctx.fillRect(x, y, w, h);
	}

	draw()
	{
		this.p1 = this.world_to_canvas(this.p1.x, this.p1.y);
		this.p2 = this.world_to_canvas(this.p2.x, this.p2.y);
		this.ball = this.world_to_canvas(this.ball.x, this.ball.y);
		this.ctx.fillStyle = "black";
		this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);		
		this.ctx.fillStyle = "red";
		this.draw_rect_by_canvas(this.p1.x, this.p1.y, 20, 100);
		this.ctx.fillStyle = "white";
		this.draw_rect_by_canvas(this.p2.x, this.p2.y, 20, 100);
		this.draw_rect_by_canvas(this.ball.x, this.ball.y, 10, 10);
		this.ctx.fillStyle = "white";
		this.ctx.font = "30px Arial";
		this.ctx.fillText(this.score.p1, 50, 30);
		this.ctx.fillText(this.score.p2, this.canvas.width - 70, 30);
		this.ctx.fillText(this.state, this.canvas.width / 2 - 50, 30);
		this.ctx.fillStyle = "white";
		this.ctx.fillRect(this.canvas.width / 2, 0, 1, this.canvas.height);
	}

	set_owner(p)
	{
		if (p == 1)
		{
			this.owner_is = 1;
		}
		else if (p == 2)
		{
			this.owner_is = 2;
		}
		else
		{
			this.owner_is = null;
		}
	}

	join_game(gameid, gamepass, player, playerpass)
	{
		var url = "/join_game";
		var endpoint = this.url;
		var data = {gameid: gameid, password: gamepass, player: player, player_pass: playerpass};
		
		return new Promise(function(resolve, reject) {
			var req = new Request(endpoint);
			req.post(url, data)
			.then(function(response) {
				if (response.ok) {
					return response.json();
				}else{
					throw new Error("HTTP error " + response.status);
				}
			})
			.then(function(data) {
				resolve(data);
			})
			.catch(function(error) {
				console.log(error);
				reject(error);
			});
		});
	}

	game_info(gameid) {
		var url = "/info/" + gameid;
		var endpoint = this.url;
		return new Promise(function(resolve, reject) {
		  var req = new Request(endpoint);
		  req.get(url)
			.then(function(response) {
			  if (response.ok) {
				return response.json();
			  } else {
				throw new Error("HTTP error " + response.status);
			  }
			})
			.then(function(data) {
			  resolve(data);
			})
			.catch(function(error) {
			  console.log(error);
			  reject(error);
			});
		});
	  }

	move(gameid, gamepass, player, playerpass, direction)
	{
		var url = "/move";
		var endpoint = this.url;
		var data = {gameid: gameid, password: gamepass, player: player, player_pass: playerpass, direction: direction};
		return new Promise(function(resolve, reject) {
			var req = new Request(endpoint);
			req.post(url, data)
			.then(function(response) {
				if (response.ok) {
					return response.json();
				}else{
					throw new Error("HTTP error " + response.status);
				}
			})
			.then(function(data) {
				resolve(data);
			})
			.catch(function(error) {
				console.log(error);
				reject(error);
			});
		});
	}

	set_parameters(gameid, gamepass, player, playerpass)
	{
		this.set_owner(player);
		this.parameters.gameid = gameid;
		this.parameters.gamepass = gamepass;
		this.parameters.player = player;
		this.parameters.playerpass = playerpass;
	}

};

export default Game;