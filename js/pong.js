const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');



dummy_token = "1234567890";
current_room = "test";

function send_ball()
{
    var type="user";
    var command = "BALL";
    var room = current_room;
    var args = {posX: ball.x, posY: ball.y, room: room}
    var data = {type: type, command: command, args: args};
    socket.send(JSON.stringify(data));
}


function send_player()
{
    var type="user";
    var command = "MOVE";
    var room = current_room;
    var args = {posX: p1.x, posY: p1.y, room: room}
    var data = {type: type, command: command, args: args};
    socket.send(JSON.stringify(data));
}

current_password = "test";

function send_join()
{
    var type="user";
    var command = "JOIN";
    var room = current_room;
    var args = {room: room, password: current_password}
    var data = {type: type, command: command, args: args};
    socket.send(JSON.stringify(data));
}

function send_get_what(what_type)
{
    var type="user";
    var command = "GET";
    var what = what_type;
    var room = current_room;
    var args = {room: room, what: what}
    var data = {type: type, command: command, args: args};
    socket.send(JSON.stringify(data));
}







const width = canvas.width = 800;
const height = canvas.height = 800;
events = 0;
window.addEventListener('keyup',keyUpListener,false);
window.addEventListener('keydown',keyDownListener,false); 

started = false;
const socket = new WebSocket('ws://localhost:8080');



socket.onopen = function(e) {
    console.log("[open] Connection established");

};

socket.onmessage = eachRecieve;

function connectionstart()
{

       
}

host = -1;

function start(data)
{

}



function eachRecieve(event)
{
    var data = JSON.parse(event.data);
    console.log(data);
 

}

function info(data)
{
    if (data.data == "host")
    {
        console.log("Host");
        host = 0;
    }
    else
    {
        console.log("server");
        host = 1;
    }
}

function updatePlayer(data)
{
        middlex = width / 2;
        middley = height / 2;

        mirrorx = middlex - data.x;
        mirrory = middley - data.y;

        p2.x = mirrorx;
        p2.y = mirrory;
}

function chekCollision(ball, player) {

    var ballLeft = ball.x;
    var ballRight = ball.x + ball.size;
    var ballTop = ball.y;
    var ballBottom = ball.y + ball.size;

    var playerLeft = player.x;
    var playerRight = player.x + player.size;
    var playerTop = player.y;
    var playerBottom = player.y + player.size + 50;

    var collision = true;

    if ((ballBottom < playerTop) ||
        (ballTop > playerBottom) ||
        (ballRight < playerLeft) ||
        (ballLeft > playerRight)) {
        collision = false;
    }

    return collision;
}


class Ball {

    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = 15;
        this.speed = 100;
        this.velcheck = 0;
        this.velocity = {
            x: 0,
            y: 0
        }
    }

    draw() {
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.size, this.size);
        ctx.fill();
    }

    changeDirection(x, y) {
        this.velocity.x = x;
        this.velocity.y = y;
    }

    collide(player) {
        return chekCollision(this, player);
    }

    update(delta) {

        if (host == false)
        {
            this.draw();
            return;
        }
        if (this.collide(p1) && this.velocity.x < 0) {
            if (this.velcheck == 0) {
                this.velocity.x = -this.velocity.x + (p1.getVelocity().x * p1.getMass());
                this.velocity.y = -this.velocity.y + p1.getVelocity().y * p1.getMass();
            }
            else
            {
                this.velocity.x = -this.velocity.x;
                this.velocity.y = -this.velocity.y;
            }
        }
        else if (this.collide(p2) && this.velocity.x > 0) {
            this.velocity.x = -this.velocity.x ;
        }
        if (this.x + this.size >= width && this.velocity.x > 0) {
            this.velocity.x = -this.velocity.x ;
        }
        if (this.y + this.size >= height && this.velocity.y > 0) {
            this.velocity.y = -this.velocity.y ;
        }
        if (this.x <= 0 && this.velocity.x < 0) {
            this.velocity.x = -this.velocity.x ;
        }
        if (this.y <= 0 && this.velocity.y < 0) {
            this.velocity.y = -this.velocity.y;
        }
        this.x += this.velocity.x * this.speed * delta;
        this.y += this.velocity.y * this.speed * delta;

        this.draw();
    }

}

class Player {
    constructor(x, y, color, type) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.type = type;
        this.size = 20;
        this.speed = 100;
        this.mass = 2;
        this.bot = false;
        this.velocity = {
            x: 0,
            y: 0
        }        
    }

    draw() {
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.size, this.size + 50);
        ctx.fill();
    }

    translate(x, y, delta) {
        this.velocity.x += x;
        this.velocity.y += y;
    }
 
    getVelocity() {
        return this.velocity;
    }
    getMass() {
        return this.mass;
    }


    motion(delta) {
        this.x += this.velocity.x * this.speed * delta;
        this.y += this.velocity.y * this.speed * delta;
        if (this.y <= 0) {
            this.y = 0;
        }
        if (this.y + this.size + 50 >= height) {
            this.y = height - this.size - 50;
        }
        if (this.x <= 0) {
            this.x = 0;
        }
        if (this.x + this.size >= width) {
            this.x = width - this.size;
        }
        this.velocity.y -= 0.2 * this.velocity.y; 
    }

    update(delta) {


        if (events != 0 && this.type == 'client') {
            if (events & 1) {
                this.translate(0, -1, delta);
                
            }
            if (events & 2) {
                this.translate(0, 1, delta);
            }
        }
        if (this.bot == false) {
            if (this.type == 'client') 
            {
                this.motion(delta);
            }
            if (started == false) {

                this.draw();
                return;
            }
            if (this.type == 'client'){

                var data = {type: "player", x: this.x, y: this.y};
                socket.send(JSON.stringify(data));
            }
             
        }
        this.draw();
    }
}




function keyDownListener(event) {
    if (event.key == 'w') {
        events = (events | 1);
    }
    if (event.key == 's') {
        events = (events | 2);
    }
}

function keyUpListener(event) {
    if (event.key == 'w') {
        events = (events ^ 1)

    }
    if (event.key == 's') {
        events = (events ^ 2)
    }
}



const psizes = {
    width: 20,
    height: 50
}
p2 = new Player(width - 30, (height / 2) - (psizes.height / 2), 'blue', 'server');
p1 = new Player(10, (height / 2) - (psizes.height / 2), 'red', 'client');
ball = new Ball(width / 2, height / 2, 'white');



function update(delta) {

    if (delta == NaN) {
        delta = 1;
    }
    p1.update(delta, ctx);
    p2.update(delta, ctx);
    ball.update(delta, ctx);
}



function init()
{
    
    window.requestAnimationFrame(loop);
}

lastTime = window.performance.now();

function loop(timestamp) {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = 'rgba(0,0,0,255)';
    ctx.fillRect(0, 0, width, height);
    var now = window.performance.now();
    var deltaTime = (now - lastTime) / 1000;
    lastTime = now;    
    update(deltaTime);
    window.requestAnimationFrame(loop);
}