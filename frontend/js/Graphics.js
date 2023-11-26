import {Player, RemotePlayer, Ball} from "./Player.js";
import UserRequest  from "./Request.js";

class PongGraphics {
	constructor(canvas, width, height) {
		this.canvas = canvas;
		this.width = width;
		this.height = height;
		this.context = canvas.getContext("2d");
	}

	drawRect(x, y, width, height, color) {
		this.context.fillStyle = color;
		this.context.fillRect(x, y, width, height);
	}

	drawCircle(x, y, radius, color) {
		this.context.fillStyle = color;
		this.context.beginPath();
		this.context.arc(x, y, radius, 0, 2 * Math.PI);
		this.context.fill();
	}

	drawText(text, x, y, color, font) {
		this.context.fillStyle = color;
		this.context.font = font;
		this.context.fillText(text, x, y);
	}

	clear() {
		this.context.clearRect(0, 0, this.width, this.height);
	}
}


class Pong
{
	constructor(canvas, width, height, socket, token)
	{
		this.graphics = new PongGraphics(canvas, width, height);
		this.socket = socket;
		this.token = token;
		this.req = new UserRequest(socket, token);
		this.room = "test";
		this.state = -1;
		this.up = 0;
		this.down = 0;
		this.player = new Player("blue", {x: 10, y: height/2}, 1);
		this.remote_player = new RemotePlayer("red", {x: width - 10, y: height/2}, 1);
		this.ball = new Ball("white", {x: width/2, y: height/2});
		this.ball.pos = {x: width/2, y: height/2};
		this.init();
	}

	init()
	{
		this.socket.onmessage = this.onmessagedata;
		this.graphics.canvas.addEventListener("keydown", this.onkeydown.bind(this));
		this.graphics.canvas.addEventListener("keyup", this.onkeyup.bind(this));
	}

	onkeydown(event)
	{
		if (event.key == "ArrowUp")
		{
			this.up = 1;
		}
		if (event.key == "ArrowDown")
		{
			this.down = 1;
		}
	}

	onkeyup(event)
	{
		if (event.key == "ArrowUp")
		{
			this.up = 0;
		}
		if (event.key == "ArrowDown")
		{
			this.down = 0;
		}
	}

	onmessagedata(event)
	{
		var data = JSON.parse(event.data);
		console.log(data);
		if (data.type == "game")
		{
			var dat = data.data;
			var command = dat.command;
			var args = dat.args;
			if (command == "ball")
			{
				var x = args.posX;
				var y = args.posY;
				console.log(x);
				console.log(y);
				this.ball.updatePos({x: x, y: y});
			}	
			if (command == "player")
			{
				this.remote_player.updatePos({x: args.posX, y: args.posY});
			}
			if (command == "winner")
			{
				this.state = 1;
			}
			if (command == "loser")
			{
				this.state = 2;
			}
			if (command == "start")
			{
				this.state = 0;
			}
		}
	}

	change_room(room, password)
	{
		this.req.request("JOIN", {name: room, password: password});
		//this.socket.send(JSON.stringify({type: "user", data: {user_token: this.token, command: "JOIN", args: {name: room, password: password}}}));
	}

	player_pos_update()
	{
		this.req.request("MOVE", {name: this.room, posX: this.player.pos.x, posY: this.player.pos.y});
		//var data = {type: "user", data: {user_token: this.token, command: "MOVE", args: {name: this.room, posX: this.player.pos.x, posY: this.player.pos.y}}};
		//this.socket.send(JSON.stringify(data));
	}

	run()
	{
		this.updates();
		this.update_draw();
		window.requestAnimationFrame(this.run.bind(this));
	}

	updates()
	{
		if (this.state == -1)
		{
			return;
		}
		if (this.up == 1)
		{
			this.player.moveUp();
		}
		if (this.down == 1)
		{
			this.player.moveDown();
		}
		this.player.tick();
		this.player_pos_update();
	}
	
	update_draw()
	{
		this.graphics.drawRect(0, 0, this.graphics.width, this.graphics.height, "black");
		this.player.draw(this.graphics.context);
		this.remote_player.draw(this.graphics.context);
		this.ball.draw(this.graphics.context);
	}

}

export default Pong;