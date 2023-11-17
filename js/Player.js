

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
}

class Player extends Paddle
{
    constructor(color, pos)
    {
        super(color, pos);
        this.name = "Player";
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


///export {Player, RemotePlayer};