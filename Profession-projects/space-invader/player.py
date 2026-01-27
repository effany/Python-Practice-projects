from turtle import *
import turtle as t
from PIL import Image
import os


if not os.path.exists('./asset/ufo-40.gif'):
    img = Image.open('./asset/ufo.gif')
    img_resized = img.resize((50,50), Image.LANCZOS)
    img_resized.save('./asset/ufo-40.gif')

t.register_shape('./asset/ufo-40.gif')

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('./asset/ufo-40.gif')
        self.penup()
        self.goto(0, -300)
        self.bullet_move = 5
        self.bullets = []
    

    def right(self):
        current_x = self.xcor()
        if current_x <= 300:
            self.goto(self.xcor() + 20, self.ycor())
            self.screen.update()

    def left(self):
        current_x = self.xcor()
        if current_x >= - 300:
            self.goto(self.xcor() - 20, self.ycor())
            self.screen.update()

    def load(self):
        if len(self.bullets) < 5:
            bullet = Turtle()
            bullet.shape('circle')
            bullet.shapesize(0.5,0.5)
            bullet.color('#488B8F')
            bullet.penup()
            bullet.goto(self.xcor(), self.ycor())
            bullet.has_hit_obstacle = False
            self.bullets.append(bullet) 
        
        
    def shoot(self):
        for bullet in self.bullets[:]:  # Iterate over copy
            if bullet.ycor() < 380:  # Check bullet position, not player
                new_y = bullet.ycor() + self.bullet_move
                bullet.goto(bullet.xcor(), new_y)
            else:
                bullet.hideturtle()
                self.bullets.remove(bullet)  # Remove bullet, not undefined player_bullet