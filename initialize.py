import turtle

def window(h, w):
    window = turtle.Screen()
    window.title("PingPong")
    window.bgcolor("blue")
    window.setup(height=h, width=w)
    window.tracer(0)  # регулювання швидкості
    return window

def player(isLeft):
    player = turtle.Turtle()
    player.speed(0)
    player.shape("square")
    player.shapesize(stretch_wid=5)
    player.color("black")
    player.penup()
    player.goto(-300 if isLeft else 300, 0)
    return player

def ball():
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 2
    ball.dy = 2
    return ball

def score():
    score = turtle.Turtle()
    score.speed(0)
    score.color("white")
    score.penup()  # щоб не малювалась лінія
    score.hideturtle()  # щоб не було видно контуру об'єкта
    score.goto(0, 260)
    score.write("Player A: 0  Player B: 0", align="center", font=("Arial", 30))
    return score