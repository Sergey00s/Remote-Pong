


class UserRequest {
	constructor(socket, token, username, userid) {
		this.socket = socket;
		this.token = token;
		this.username = username;
		this.userid = userid;
	}

	set_token(token) {
		this.token = token;
	}

	set_username(username) {
		this.username = username;
	}

	set_userid(userid) {
		this.userid = userid;
	}

	send_playermove(x, y, roomid, dataset) {
		var data = {
			usertoken: this.token,
			username: this.username,
			userid: this.userid,
			message: {
				type: "gameupdate",
				data: {
					roomid: roomid,
					type: "playermove",
					data: {
						playerposx: dataset.playerposx,
						playerposy: dataset.playerposy,
						playervelx: dataset.playervelx,
						playervely: dataset.playervely,
						playermomentumx: dataset.playermomentumx,
						playermomentumy: dataset.playermomentumy
					}
				}
			}
		};
		this.socket.send(JSON.stringify(data));
	}

	send_room_command(roomid, command) {
		var data = {
			usertoken: this.token,
			username: this.username,
			userid: this.userid,
			message: {
				type: command,
				data: {
					roomid: roomid
				}
			}
		};
		this.socket.send(JSON.stringify(data));	
	}

	send_ready(roomid) 
	{
		var data = {
			usertoken: this.token,
			username: this.username,
			userid: this.userid,
			message: {
				type: "gameupdate",
				data: {
					roomid: roomid,
					type: "playerready",
					data: {
						playerready: true
					}
				}
			}
		};
		this.socket.send(JSON.stringify(data));
	}
}

export default UserRequest;
