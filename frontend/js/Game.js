
class Logic
{
	constructor(canvas, socket, id) 
	{
		this.canvas = canvas;
		this.socket = socket;
		this.id = id;
		this.ctx = canvas.getContext("2d");
		this.ctx.fillStyle = "black";
		this.ball = {
			posx: 200,
			posy: 200,
		}

		this.player = {
			posx: 0,
			posy: 0,
			velx: 0,
			vely: 0,
			momx: 0,
			momy: 0
		}

		this.remoteplayer = {
			posx: 0,
			posy: 0,
		}

	}

	is_player_collide_wall()
	{
		if (this.player.posy < 0 || (this.player.posy + 50 ) > this.canvas.height)
		{
			return true;
		}
		return false;
	}

	calculate_momentum()
	{
		this.player.momx = this.player.velx * 0.1;
		this.player.momy = this.player.vely * 0.1;
	}

	init()
	{
		this.player.posx = 10;
		this.player.posy = this.canvas.width / 2;
		this.player.velx = 0;
		this.player.vely = 0;
		this.player.momx = 0;
		this.player.momy = 0;
		this.inputs();
		window.requestAnimationFrame(this.update.bind(this));

	}

	render()
	{
		//this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
		this.ctx.fillStyle = "black";
		this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
		this.ctx.fillStyle = "white";
		this.ctx.fillRect(this.player.posx, this.player.posy, 10, 50);
		this.ctx.fillRect(this.remoteplayer.posx, this.remoteplayer.posy, 10, 50);
		this.ctx.fillRect(this.ball.posx, this.ball.posy, 5, 5);
	}

	inputs()
	{
		window.addEventListener("keydown", function(event)
		{
			switch(event.key)
			{
				case "ArrowUp":
					this.player.vely += -1;
					break;
				case "ArrowDown":
					this.player.vely += 1;
					break;
				default:
					break;
			}
		}.bind(this));
	}

	send_player_pos()
	{
		var msg = {
			type: "playerpos",
			playerid: this.id,
			posx: this.player.posx,
			posy: this.player.posy,
			velx: this.player.velx,
			vely: this.player.vely,
			momx: this.player.momx,
			momy: this.player.momy
		}
		this.socket.send(JSON.stringify(msg));
	}

	update()
	{
		this.calculate_momentum();
		this.player.posx += this.player.velx;
		this.player.posy += this.player.vely;
		this.player.velx += this.player.momx;
		this.player.vely += this.player.momy;
		if (this.is_player_collide_wall())
		{
			this.player.posx -= this.player.velx;
			this.player.posy -= this.player.vely;
			this.player.velx = 0;
			this.player.vely = 0;
			this.player.momx = 0;
			this.player.momy = 0;
		}
		this.player.velx *= 0.9;
		this.player.vely *= 0.9;
		if  (Math.abs(this.player.velx) < 0.1)
		{
			this.player.velx = 0;
		}
		if  (Math.abs(this.player.vely) < 0.1)
		{
			this.player.vely = 0;
		}

		this.render();
		this.send_player_pos();
		window.requestAnimationFrame(this.update.bind(this));
	}
}




class Game
{
	constructor(self_token, canvas, socket, id) 
	{
		this.self_token = id;
		this.socket = socket;
		this.gamestatus = "waiting";
		this.socket.onmessage = this.onmessage.bind(this);
		this.canvas = canvas;
		this.ctx = canvas.getContext("2d");
		var msg ={
			type: "join",
			playerid: this.self_token
		}
		this.socket.send(JSON.stringify(msg));
		this.logic = new Logic(this.canvas, this.socket, this.self_token);		
	}

	get_ready()
	{
		var msg = {
			type: "meready",
			playerid: this.self_token
		}
		this.socket.send(JSON.stringify(msg));
		this.gamestatus = "ready";
	}

	onmessage(event)
	{
		var msg = JSON.parse(event.data);
		switch(msg.type)
		{
			case "winner":
				console.log("Game is over you won");				
				break;
			case "loser":
				console.log("Game is over you lost");
				break;
			case "ball":
				console.log ("ball update")
				this.logic.ball.posx = msg.x;
				this.logic.ball.posy = msg.y;
				break;
			case "starting":
				console.log("Game is starting");
				this.gamestatus = "playing";
				this.logic.init();
				break;
			case "playerpos":
				console.log("player pos");
				this.logic.remoteplayer.posx = msg.posx;
				this.logic.remoteplayer.posy = msg.posy;
				break;
			case "beready":
				this.get_ready();
				break;
			default:
				console.log(msg);
				console.log("Unknown message type: " + msg.type);
				break;
		}
	}

	player_pos()
	{
		var msg = {
			type: "playerpos",
			playerid: this.self_token,
			posx: 0,
			posy: 0,
			velx: 0,
			vely: 0,
			momx: 0,
			momy: 0
		}
		this.socket.send(JSON.stringify(msg));
	}
}



export default Game;