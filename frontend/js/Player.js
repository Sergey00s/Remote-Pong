

class Ball{

    constructor(x, y)
    {
        this.x = x;
        this.y = y;
    }

    draw(ctx)
    {
        ctx.rect(this.x, this.y, 10, 10);
    }

    new_position(x, y)
    {
        this.x = x;
        this.y = y;
    }
};



class Player{

    constructor(x, y, height, width)
    {
        this.x = x;
        this.y = y;
    }

    draw(ctx)
    {
        ctx.rect(this.x, this.y, 10, 10);
    }

    new_position(x, y)
    {
        this.x = x;
        this.y = y;
    }



};



export { Ball, Player };