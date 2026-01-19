from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

class BlocksManager:
    def __init__(self):
        self.blocks = []
    
    def create_line_blocks(self, start, y_pos):
        x_shape_var = [1, 2, 4, 5, 8, 10, 20]
        current_x = start  
        while current_x < 400:  
            random_x = int(random.choice(x_shape_var))
            block_width = random_x * 20
            block_center = current_x + block_width / 2  # Center is halfway into the block
            
            # Create individual block turtle
            block = Turtle()
            block.shape("square")
            block.shapesize(stretch_wid=2, stretch_len=random_x)
            block.color(random.choice(COLORS))
            block.penup()
            block.goto(block_center, y_pos)
            
            self.blocks.append(block)
            current_x += block_width  # Move to the RIGHT EDGE of current block

    def stack_line_blocks(self, y_pos):
        self.create_line_blocks(-400, y_pos)