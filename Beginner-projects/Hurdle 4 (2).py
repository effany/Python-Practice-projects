def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
def turn_around():
    turn_left()
    turn_left()    

def loop():
    move()
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()
  
def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()
    

def move_until_right_is_open():
    while wall_on_right() and not at_goal():
        if front_is_clear():
            move()
        else:
            turn_left()
            
    
while not at_goal():
    if wall_in_front() and wall_on_right():
        move_until_right_is_open()
        if at_goal():
            break

        turn_right()
        if front_is_clear():
            move()
            if at_goal():
                break

        turn_right()
        if front_is_clear():
            move()
            if at_goal():
                break

    elif front_is_clear():
        move()
        if at_goal():
            break
       
        
        
     
   
        
        
       

    

################################################################
# WARNING: Do not change this comment.
# Library Code is below.
################################################################
