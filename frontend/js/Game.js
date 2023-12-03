import {Player, Ball} from "./Player.js";


class Pong
{
	constructor(canvas, socket, id)
	{
		this.canvas = canvas;
		this.socket = socket;
		this.id = id;
		this.score1 = 0;
		this.score2 = 0;
		this.ready = false;
		this.ctx = canvas.getContext("2d");
		this.ctx.fillStyle = "black";
		this.ctx.fillRect(0, 0, canvas.width, canvas.height);
		this.ball = new Ball(canvas.width/2, canvas.height/2);
		this.player = new Player(10, canvas.height/2, 10, 50);
		this.remoteplayer = new Player(canvas.width - 10, canvas.height/2, 10, 50);
		this.socket.onmessage = this.onmessage.bind(this);
		//window.addEventListener("keydown", this.keydown.bind(this));

	}

	keydown(event)
	{
		if(event.keyCode == 38)
		{
			this.socket.send(JSON.stringify({"type": "move", "direction": "up", "token": this.id}));
		}
		if(event.keyCode == 40)
		{
			this.socket.send(JSON.stringify({"type": "move", "direction": "down", "token": this.id}));
		}
	}


	to_screen_coords(x, y)
	{
		var canvas_width = this.canvas.width;
		var canvas_height = this.canvas.height;
		var world_width = 1000;
		var world_height = 1000;


		var x_screen = (x / world_width) * canvas_width;
		var y_screen = (y / world_height) * canvas_height;

		return [x_screen, y_screen];

	}



	onmessage(event)
	{
		var data = JSON.parse(event.data);
		console.log(data);
		if(data.type == "new_position")
		{
			var coords = this.to_screen_coords(data.x, data.y);
			this.remoteplayer.new_position(coords[0], coords[1]);
		}
		if (data.type == "new_ball_position")
		{
			var coords = this.to_screen_coords(data.x, data.y);
			this.ball.new_position(coords[0], coords[1]);
		}
		if (data.type == "score1")
		{
			this.score1 = this.score1 + 1;
		}
		if (data.type == "score2")
		{
			this.score2 = this.score2 + 1;
		}
		
	}


	
};


export default Pong;