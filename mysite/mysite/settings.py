from turtle import *
from random import choice
from time import sleep

scr = Screen()
canvas = scr.getcanvas()
root = canvas.winfo_toplevel()

scr.setup(600, 400)
scr.title('Ping-Pong')
scr.cv._rootwindow.resizable(False, False)


def on_close():
    global running
    running = False
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
running = True

penup()
hideturtle()
setposition(0, 150)
write(f'Красный: 0           Синий: 0', font=("Arial", 20, "bold"), align="center")

lst = [30, 60, 120, 150, 210, 240, 300, 330]


class Sprint(Turtle):
    score = 0

    def __init__(self, x, width, height, color_, shape="square"):
        super().__init__(shape)
        self.color(color_)
        self.x = x
        self.shapesize(width, height)

    def change_settings(self):
        self.penup()
        self.speed(0)
        self.setposition(self.x, 0)

    def move_up(self):
        x, y = self.pos()
        if y <= 150:
            self.setposition(x, y + 20)

    def move_down(self):
        x, y = self.pos()
        if y >= -140:
            self.setposition(x, y - 20)


class Ball(Turtle):
    def __init__(self, shape="circle"):
        super().__init__(shape)

    def change_settings(self):
        self.penup()
        self.speed(0)
        self.shapesize(0.7)
        self.setheading(choice(lst))

    def go(self, enemy1, enemy2):
        while running:
            self.forward(2.5)
            if self.ycor() >= 190:
                self.setheading(360 - self.heading())
            elif self.ycor() <= -180:
                self.setheading(360 - self.heading())

            if self.xcor() < -300:
                self.setposition(0, 0)
                self.setheading(choice(lst))
                enemy2.score += 1
                clear()
                write(f'Красный: {enemy1.score}           Синий: {enemy2.score}', font=("Arial", 20, "bold"),
                      align="center")
            elif self.xcor() > 300:
                self.setposition(0, 0)
                self.setheading(choice(lst))
                enemy1.score += 1
                clear()
                write(f'Красный: {enemy1.score}           Синий: {enemy2.score}', font=("Arial", 20, "bold"),
                      align="center")

            if -179 > self.xcor() > -181 and abs(self.ycor() - enemy1.ycor()) <= 50:
                self.setheading(180 - self.heading())
                self.forward(2)

            if 179 < self.xcor() < 181 and abs(self.ycor() - enemy2.ycor()) <= 50:
                self.setheading(180 - self.heading())
                self.forward(2)


t1 = Sprint(-200, 4, 1, 'red')
t1.change_settings()
t2 = Sprint(200, 4, 1, 'blue')
t2.change_settings()

ball = Ball()
ball.change_settings()

scr.listen()
onkey(t1.move_up, 'w')
onkey(t1.move_down, 's')

onkey(t2.move_up, 'Up')
onkey(t2.move_down, 'Down')

ball.go(t1, t2)