from turtle import Turtle, Screen
import turtle as t 
from spaceship_manager import SpaceShipManager
from obstacles_manager import ObstacleManager
from bullet import Bullet
from player import Player
import random
import time

my_screen = Screen()
my_screen.setup(width=800, height=800)
my_screen.bgcolor("white")
my_screen.tracer(0)
# create initial spaceships
x = -150

ships = []

# Get the window size you set
width = my_screen.window_width()
height = my_screen.window_height()

for i in range(8):
    ships.append(SpaceShipManager(x, 300))
    ships.append(SpaceShipManager(x, 250))
    ships.append(SpaceShipManager(x, 200))
    x += 40

my_screen.update()

obstacle_manager = ObstacleManager("Cum Shoot Me")
player = Player()
my_screen.listen()

bullet_timer = 0
alien_bullets = []  

def collide_removal_check(x_array, y_array):
    if x_array and y_array:  # Check if lists are not empty
        to_remove_x = []
        to_remove_y = []
        
        for x in x_array:
            for y in y_array:
                if x.distance(y) < 20:
                    to_remove_x.append(x)
                    to_remove_y.append(y)
                    x.hideturtle()
                    y.hideturtle()
        
        # Remove after iteration
        for x in to_remove_x:
            if x in x_array:
                x_array.remove(x)
        for y in to_remove_y:
            if y in y_array:
                y_array.remove(y)

while True:
    my_screen.update()
    for ship in ships:
        ship.move()
        current_x = ship.xcor()
        cuurent_y = ship.ycor()

        if current_x > 300:
            ship.bounce_x()
            ship.move()
        elif current_x < -300:
            ship.bounce_x()
            ship.move()
    
    # Move all active bullets
    for bullet in alien_bullets:
        bullet.drop()
    
    player.shoot()
    
    # Create new bullets periodically
    bullet_timer += 1
    if bullet_timer > 30:
        random_ship = random.choice(ships)
        bullet = Bullet(random_ship.xcor(), random_ship.ycor())
        alien_bullets.append(bullet)
        bullet_timer = 0

    my_screen.onkeypress(key="Right", fun=player.right)
    my_screen.onkeypress(key="Left", fun=player.left)
    my_screen.onkeypress(key="space", fun=player.load)

    ## gaming logic

    collide_removal_check(ships, player.bullets)
    
    for bullet in alien_bullets[:]:  
        hit_this_frame = False
        for obstacle in obstacle_manager.font_stamps_array[:]:
            if bullet.distance(obstacle["position"]) < 20:
                obstacle_manager.clearstamp(obstacle["id"])
                obstacle_manager.font_stamps_array.remove(obstacle)
                bullet.has_hit_obstacle = True  # Mark that this bullet hit an obstacle
                hit_this_frame = True
        
        # If bullet previously hit obstacles and is now past the obstacle zone, remove it
        if bullet.has_hit_obstacle and not hit_this_frame:
            bullet.hideturtle()
            alien_bullets.remove(bullet)

    for player_bullet in player.bullets[:]:  
        hit_this_frame = False
        for obstacle in obstacle_manager.font_stamps_array[:]:
            if player_bullet.distance(obstacle["position"]) < 20:
                obstacle_manager.clearstamp(obstacle["id"])
                obstacle_manager.font_stamps_array.remove(obstacle)
                player_bullet.has_hit_obstacle = True  # Mark that this bullet hit an obstacle
                hit_this_frame = True
        
        # If bullet previously hit obstacles and is now past the obstacle zone, remove it
        if player_bullet.has_hit_obstacle and not hit_this_frame:
            player_bullet.hideturtle()
            player.bullets.remove(player_bullet)
    
    for player_bullet in player.bullets[:]:
        for alien_bullet in alien_bullets:
            if player_bullet.distance(alien_bullet) < 20:
                player_bullet.hideturtle()
                alien_bullet.hideturtle()
                alien_bullets.remove(alien_bullet)
                player.bullets.remove(player_bullet)
            
    ## game over logic

    if len(ships) == 0:
        print("game over!")
        exit()
    for bullet in alien_bullets:
        if bullet.distance(player) < 20:
            print("Game Over!")
            exit()
   



my_screen.exitonclick()