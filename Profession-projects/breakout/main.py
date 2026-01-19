from turtle import Screen
from blocks_manager import BlocksManager
from paddle import Paddle
from balls import Ball
import random

screen = Screen()
screen.setup(width=800, height=600)
screen.title("My Breakout Game")
screen.tracer(0)


block_manager = BlocksManager()
paddle = Paddle()
ball = Ball()

# create initial blocks
starting_y_pos = 300
for i in range(6):
    block_height = 20*2  # 80 pixels
    y_block_center = starting_y_pos - block_height / 2  # Center of current row
    block_manager.stack_line_blocks(y_block_center)
    starting_y_pos -= block_height  # Move down by full block height

current_blocks = block_manager.blocks


screen.listen()
screen.onkey(key="Left", fun=paddle.left)
screen.onkey(key="Right", fun=paddle.right)

game_on = True

while game_on:
    screen.update()
    ball.move()

    # Wall bounce
    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.bounce_x()
    
    # Top wall bounce
    if ball.ycor() > 290:
        ball.bounce_y()
    
    # calculate paddle area
    paddle_width = 20 * paddle.shapesize()[1] 
    paddle_left = paddle.xcor() - paddle_width / 2
    paddle_right = paddle.xcor() + paddle_width /2

    # Ball boundaries (assuming ball radius is 10 pixels)
    ball_radius = 10
    ball_left = ball.xcor() - ball_radius
    ball_right = ball.xcor() + ball_radius
    ball_top = ball.ycor() + ball_radius
    ball_bottom = ball.ycor() - ball_radius

    # Paddle bounce - check if ball is moving down and overlapping with paddle
    if (ball_right >= paddle_left and ball_left <= paddle_right and 
        ball.ycor() < -230 and ball.y_move < 0):
        ball.bounce_y()
    
    # Loss condition
    if ball.ycor() < -290:
        print("You lost")
        exit()
    
    if ball.ycor() > 290 or len(current_blocks) == 0:
        print("You WIN!")
    
    # Find the closest block that the ball is actually overlapping with
    closest_block = None
    min_distance = float('inf')
    for block in current_blocks:
        # Get block dimensions (shapesize returns (height_stretch, width_stretch))
        block_height = 20 * 2  # 40 pixels (stretched by 2)
        block_width = 20 * block.shapesize()[1]  # Width depends on stretch_len
        
        # Calculate block boundaries
        block_left = block.xcor() - block_width / 2
        block_right = block.xcor() + block_width / 2
        block_top = block.ycor() + block_height / 2
        block_bottom = block.ycor() - block_height / 2
        
        # Check if ball overlaps with block
        if (ball_right >= block_left and ball_left <= block_right and
            ball_top >= block_bottom and ball_bottom <= block_top):
            # Ball is overlapping this block, check if it's the closest
            distance = ball.distance(block)
            if distance < min_distance:
                min_distance = distance
                closest_block = block
    
    # Remove only the closest block that's actually being hit
    if closest_block:
        ball.bounce_y()
        closest_block.hideturtle()
        current_blocks.remove(closest_block)
        ball.increase_speed()
    
    
    



screen.exitonclick() 
