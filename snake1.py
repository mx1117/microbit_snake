# Direction code:
#   px - positive x
#   nx - negative x
#   py - positive y
#   ny - negative y

from microbit import *
from random import randint

snake = [[0, 0]]
snake_length = 2
current_fruit_location = [2,2]

direction = "px"

def reset_game():
    
    global snake
    global snake_length
    global current_fruit_location
    global direction
    
    snake = [[0, 0]]
    snake_length = 1
    current_fruit_location = [2,2]
    direction = "px"

def collision_check():
    
    global snake
    
    dup_snake = snake[:-1]
        
    if snake[-1] in dup_snake:
        
        return True
        
    return False

def add_fruit():

    global current_fruit_location
    
    current_fruit_location = [randint(0,4), randint(0,4)]
    
    while current_fruit_location in snake:
        
        current_fruit_location = [randint(0,4), randint(0,4)]
        
    display.clear()

def move_snake():
    
    global snake
    global snake_length
    
    if direction == "px":
        
        snake.append([(snake[-1][0]+1)%5, snake[-1][1]])
        
    elif direction == "nx":
        
        snake.append([(snake[-1][0]-1)%5, snake[-1][1]])
        
    elif direction == "py":
        
        snake.append([snake[-1][0], (snake[-1][1]+1)%5])
        
    elif direction == "ny":
        
        snake.append([snake[-1][0], (snake[-1][1]-1)%5])
        
    if snake_length < len(snake):
        
        snake.pop(0)
                
    if snake[-1] == current_fruit_location:
        
        snake_length += 1
        add_fruit()
        
def detect_direction_change():
    
    global direction
    
    if button_a.was_pressed():
        
        if direction == "px":
            
            direction = "ny"
            
        elif direction == "ny":
            
            direction = "nx"
            
        elif direction == "nx":
            
            direction = "py"
            
        elif direction == "py":
            
            direction = "px"
    
    if button_b.was_pressed():
        
        if direction == "px":
            
            direction = "py"
            
        elif direction == "py":
            
            direction = "nx"
            
        elif direction == "nx":
            
            direction = "ny"
            
        elif direction == "ny":
            
            direction = "nx"

while True:
    
    display.clear()
   
    detect_direction_change()
    move_snake()
    
    for piece in snake:
        
        display.set_pixel(piece[0], piece[1], 9)
        
    display.set_pixel(current_fruit_location[0], current_fruit_location[1], 4)
    
    if collision_check():
        
        display.clear()
        display.scroll("GAME OVER", wait=True, loop=False)
        
        reset_game()
    
    sleep(500)
        
        
