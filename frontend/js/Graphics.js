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
	constructor(canvas, width, height, socket, token, username, userid, roomid)
	{
		this.graphics = new PongGraphics(canvas, width, height);
		this.socket = socket;
		this.token = token;
		this.req = new UserRequest(socket, token, username, userid);
		this.roomid = roomid;
		this.username = username;
		this.userid = userid;
		this.state = "waiting";
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

	on_statuss(data)
	{
		if (data.status == "waiting")
		{
			this.state = "waiting";
		}
		if (data.status == "playing")
		{
			this.state = "playing";
		}
		if (data.status == "gameover")
		{
			this.state = "gameover";
		}
		if (data.status == "beready")
		{
			this.state = "ready";
			this.req.send_ready(this.roomid);
		}
	}

	onmessagedata(event)
	{
		var data = JSON.parse(event.data);
		console.log(data);
		if (data.type == "gameupdate")
		{
			data = data.data;
			if (data.type == "status")
				this.on_statuss(data.data);
			if (data.type == "playermove")
				this.on_playermove(data.data);
			if (data.type == "ballmove")
				this.on_ballmove(data.data);

		}
	}



	run()
	{
		this.updates();
		this.update_draw();
		window.requestAnimationFrame(this.run.bind(this));
	}

	updates()
	{
		if (this.state != "readytest")
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