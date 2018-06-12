from microbit import *
import random


class Pixel:
    def __init__(self, xPos=0, yPos=0, brightness=7):
        self.x = xPos
        self.y = yPos
        self.brightness = brightness

class Snake:
    #Dimensions of the play area
    cls_x_size = 5
    cls_y_size = 5

    cls_directions = ["UP", "RIGHT", "DOWN", "LEFT"]

    def __init__(self):
        self.direction = 1
        self.body_segments = []
        #Start the snake at x:0 Y:3
        self.body_segments.append(Pixel(0,3,9))

    def turn_anticlockwise(self):
        l = len(Snake.cls_directions)
        self.direction = (self.direction + (l - 1)) % l

    def turn_clockwise(self):
        l = len(Snake.cls_directions)
        self.direction = (self.direction + 1) % l

    def move(self, increase_size = False):
        tail = self.body_segments[-1]
        prev_segment = None
        for index, segment in reversed(list(enumerate(self.body_segments))):
            #If not the head, move segments to position of the segment ahead of it
            if index > 0:
                prev_segment = self.body_segments[index - 1]
                segment.x = prev_segment.x
                segment.y = prev_segment.y
            #If the head, we move it in the direction we're facing
            else:
                if Snake.cls_directions[self.direction] == "UP":
                    self.body_segments[0].y = (self.body_segments[0].y + ( Snake.cls_y_size - 1 )) % Snake.cls_y_size
                elif Snake.cls_directions[self.direction] == "RIGHT":
                    self.body_segments[0].x = (self.body_segments[0].x + 1) % Snake.cls_x_size
                elif Snake.cls_directions[self.direction] == "DOWN":
                    self.body_segments[0].y = (self.body_segments[0].y + 1) % Snake.cls_y_size
                elif Snake.cls_directions[self.direction] == "LEFT":
                    self.body_segments[0].x = (self.body_segments[0].x + ( Snake.cls_x_size - 1 )) % Snake.cls_y_size
        
        if increase_size:
            self.body_segments.append(Pixel(tail.x, tail.y))
        return self.check_collision()

    def check_collision(self):
        #Ignore the first element (the head doesn't colide with itself)
        head = self.body_segments[0]
        iterSeg = iter(self.body_segments)
        next(iterSeg)

        for segment in iterSeg:
            if head.x == segment.x and head.y == segment.y:
                return True

        return False

    def render(self):
        for segment in snake.body_segments:
            display.set_pixel(segment.x, segment.y, segment.brightness)

class Snake_Food(Pixel):
    def __init__(self, snake):
        coords = self.generate_coords(snake)
        super(Snake_Food, self).__init__(coords[0], coords[1], 9)

    def generate_coords(self, snake):
        x = y = None
        #Lets ensure that the food isn't on the snake
        while True:
            x = random.randint(0,4)
            y = random.randint(0,4)
            found = False
            for segment in snake.body_segments:
                if (x == segment.x) and (y == segment.y):
                    found = True
                    break
            if found:
                continue
            else:
                break

        return [x,y]

    def render(self):
        display.set_pixel(self.x, self.y, self.brightness)

display.show(Image.SNAKE)
sleep(1000)

snake = Snake()
food = Snake_Food(snake)
while True:
    #Check input
    if button_a.was_pressed():
        snake.turn_anticlockwise()
    if button_b.was_pressed():
        snake.turn_clockwise()

    #Check if we've eaten the food
    food_collide = (snake.body_segments[0].x == food.x) and (snake.body_segments[0].y == food.y)
    if snake.move(food_collide):
            break
    if not food_collide:
        #Generate new coordinates for the food
        coords = food.generate_coords(snake)
        food.x = coords[0]
        food.y = coords[1]

    display.clear()
    #Render the snake over the top of the food
    food.render()
    snake.render()
    sleep(500)

#Show the game over sad face
display.show(Image.SAD)
