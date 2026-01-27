from turtle import *
import turtle as t
from PIL import Image, ImageDraw, ImageFont

class ObstacleManager(Turtle):
    def __init__(self, words):
        super().__init__()
        self.penup()
        self.goto(-150, 0)
        self.shape('square')
        self.hideturtle()
        self.shapesize(0.2, 0.2)
        img = Image.new('1', (500, 150), 0)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
        draw.text((15,15), words, fill=1, font=font)
        self.font_stamps_array = []

        for y in range(img.height):
            for x in range(img.width):
                if img.getpixel((x,y)):
                    self.goto(x*2 - 350, (img.height - y)*2 - 250)
                    self.color('#FFC4D0')
                    stamp_id = self.stamp()
                    stamp_position = self.position()
                    self.font_stamps_array.append(
                        {"id": stamp_id,  
                        "position": stamp_position})
                    
                    