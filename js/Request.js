


class UserRequest {
	constructor(socket, token) {
		this.socket = socket;
		this.type = "user";
		this.token = token;
	}

	request(command, args) {
		var fixed_data = {type: this.type, data: {user_token: this.token, command: command, args: args}};
		this.socket.send(JSON.stringify(fixed_data));
	}

	set_token(token) {
		this.token = token;
	}
}

