class Ball
{
    constructor(color, pos)
    {
        this.color = color;
        this.pos = pos;
    }

    draw(ctx)
    {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.pos.x, this.pos.y, 5, 0, 2 * Math.PI);
        ctx.fill();
    }

    updatePos(newPos)
    {
        this.pos = newPos;
    }

}

class Paddle
{
    constructor(color, pos)
    {
        this.color = color;
        this.pos = pos;
        this.width = 10;
        this.height = 50;
        this.center = {x: this.pos.x + this.width/2, y: this.pos.y + this.height/2};
        this.pos = this.center;
        this.score = 0;
    }

    draw(ctx)
    {
        ctx.fillStyle = this.color;
        var topLeft = {x: this.pos.x - this.width/2, y: this.pos.y - this.height/2};
        ctx.fillRect(topLeft.x, topLeft.y, this.width, this.height);
    }

    updatePos(newPos)
    {
        this.pos = newPos;
    }

    updateScore(newScore)
    {
        this.score = newScore;
    }

    isCollide(ball)
    {
        var topLeft = {x: this.pos.x - this.width/2, y: this.pos.y - this.height/2};
        var bottomRight = {x: this.pos.x + this.width/2, y: this.pos.y + this.height/2};
        if (ball.pos.x >= topLeft.x && ball.pos.x <= bottomRight.x)
        {
            if (ball.pos.y >= topLeft.y && ball.pos.y <= bottomRight.y)
            {
                return true;
            }
        }
        return false;
    }

    isCollide_border()
    {
        var topLeft = {x: this.pos.x - this.width/2, y: this.pos.y - this.height/2};
        var bottomRight = {x: this.pos.x + this.width/2, y: this.pos.y + this.height/2};
        if (topLeft.y <= 0 || bottomRight.y >= 800)
        {
            return true;
        }
        return false;
    
    }
}

class Player extends Paddle
{
    constructor(color, pos, mass)
    {
        super(color, pos);
        this.name = "Player";
        this.mass = mass;
        this.velocity = {x: 0, y: 0};
        this.momentum = this.calculateMomentum();
        this.input = 0;
    }

    resolve_input()
    {
        ;
    }

    calculateMomentum()
    {
        self.momentum = self.mass * self.velocity;
        return self.momentum;
    }

    tick()
    {
        if (this.isCollide_border())
        {
            this.velocity.y *= -1;
        }
        this.pos.x += this.velocity.x;
        this.pos.y += this.velocity.y;
        this.center = this.pos;
        this.momentum = this.calculateMomentum();
        this.friction();
    }

    moveUp()
    {
        this.velocity.y -= 1;
    }
    moveDown()
    {
        this.velocity.y += 1;
    }

    friction()
    {
        this.velocity.x *= 0.9;
        this.velocity.y *= 0.9;
    }

}

class RemotePlayer extends Paddle
{
    constructor(color, pos)
    {
        super(color, pos);
        this.name = "RemotePlayer";
    }
}


export {Player, RemotePlayer, Ball};