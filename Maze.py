def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
def turn_around():
    turn_left()
    turn_left()    
  
def jump():
    turn_left()
    while wall_on_right():
        move()
    turn_left()
    while front_is_clear():
        move()
    turn_left()
    
    
while not at_goal():
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()
    
        
 
    
        
        
     
   
        
        
       

    

################################################################
# WARNING: Do not change this comment.
# Library Code is below.
################################################################
