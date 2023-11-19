

class Protocol
{
	constructor(room, password)
	{
		this.room = room;
		this.password = password;
	}

	//get remote player position
	get_remote_pPos()
	{
		var type="user";
		var command = "GET";
		var what = "pPos";
		var args = {room: this.room, what: what}
		var data = {type: type, command: command, args: args};
		return data;
	}

	//get score update
	get_score()
	{
		var type="user";
		var command = "GET";
		var what = "score";
		var args = {room: this.room, what: what}
		var data = {type: type, command: command, args: args};
		return data;
	}

	//get ball position

	get_ballPos()
	{
		var type="user";
		var command = "GET";
		var what = "ballPos";
		var args = {room: this.room, what: what}
		var data = {type: type, command: command, args: args};
		return data;
	}

	//get if server asks 
	get_ask()
	{
		var type="user";
		var command = "GET";
		var what = "ask";
		var args = {room: this.room, what: what}
		var data = {type: type, command: command, args: args};
		return data;
	}

	get_state()
	{
		var type="user";
		var command = "GET";
		var what = "state";
		var args = {room: this.room, what: what}
		var data = {type: type, command: command, args: args};
		return data;
	}

	post_pPos(x, y)
	{
		var type="user";
		var command = "PPOS";
		var room = this.room;
		var args = {posX: x, posY: y, room: this.room}
		var data = {type: type, command: command, args: args};
		return data;
	}

	post_momentum_and_velocity(x, y)
	{
		var type="user";
		var command = "PandV";
		var room = this.room;
		var args = {posX: x, posY: y, room: this.room}
		var data = {type: type, command: command, args: args};
		return data;
	}

}


export default Protocol;