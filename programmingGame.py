import turtle
import math
import random
import json
import os

#set the starting window parameters
window = turtle.Screen()
window.bgcolor = "black"
window.title("Maze Game")
window.setup(700,700)


class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.color("black")
        self.shape("square")
        self.penup()

class Treasure(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("square")    
        self.color("yellow")
        self.penup()
        self.speed(0)   
        self.gold = 100
        self.goto(x,y)

    def destroy(self): # there is no built in destoy method, so i had to do one bymyself, which simply transfroms the position of the object far from camera's boundaries
        self.hideturtle()
        self.goto(2000, 2000)
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0
        
    def go_up(self): # transform y pos by 24 pixels (up)
        move_to_x = self.xcor()
        move_to_y = self.ycor()+24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
    
    def go_down(self): #transfrom y pos by 24 pixels (down)
        move_to_x = self.xcor()
        move_to_y = self.ycor()-24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self): #transfrom x pos by 24 pixels (right)
        move_to_x = self.xcor()+24
        move_to_y = self.ycor()
        #check if the point where the player wants to go is not a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
    
    def go_left(self): #transfrom x pos by 24 pixels (left)
        move_to_x = self.xcor()-24
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self,other): # calculate the collision by comparing distance between player and other object
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if distance < 5:
            return True
        else:
            return False
class Enemy(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("square")    
        self.color("red")
        self.penup()
        self.speed(0)   
        self.gold = 25
        self.goto(x,y)
        self.direction = random.choice(["up","down","left","right"]) # random direction where to go

    def move(self): # essentially the same as players movement, except that enemy class is autonomy, while player movement will require response from the user
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0
        
        if self.is_close(player): # if enemy is close to the player -> follow him
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"


        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if(move_to_x, move_to_y) not in walls: # move only if the expected future position won't overlap with a wall, else -> choose other direction
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up","down","left","right"])

        turtle.ontimer(self.move, t = random.randint(100,300))

    def destroy(self): # there is no built in destoy method, so i had to do one bymyself, which simply transfroms the position of the object far from camera's boundaries
        self.goto(2000,2000)
        self.hideturtle()

    def is_close(self,other): # the same as players method
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if distance < 500:
            return True
        else:
            return False
def save_level_index(data, filename = "save_file.json"):
    with open(filename, "w") as f:
        json.dump(data, f)
# Function to load the level index 
def load_level_index(filename="save_file.json"):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {"level_index": 1}  # Default value in dictionary form
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            if isinstance(data, dict) and "level_index" in data:
                return data  # Return the data if it's in the correct format
            else:
                return {"level_index": 1}  # Return a default dictionary if not in the correct format
    except (FileNotFoundError, json.JSONDecodeError):
        return {"level_index": 1}  # Default dictionary in case of errors

# Loading and using the current level index
current_level_data = load_level_index()  
current_level_index = current_level_data["level_index"] 

playerdata = {
    "level_index": current_level_index,  
}
save_level_index(playerdata)  
levels = [""]
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXX         T         XXX",
"XXXXXXXXXX  E  XXXXXXXXXX",
"XXX                   XXX",
"XXX XXXXXXXX XXXXXXXX XXX",
"XXX XXXXXXXX XXXXXXXX XXX",
"XXX  XXXXXXX XXXXXXX  XXX",
"XXXX  XXXXXX XXXXXX  XXXX",
"XXXXX  XXXXX XXXXX  XXXXX",
"XXXXXX  XXXX XXXX  XXXXXX",
"XXXXXXX  XXX XXX  XXXXXXX",
"XXXXXXXX  XX XX  XXXXXXXX",
"XXXXXXXXX  X X  XXXXXXXXX",
"XXXXXXXXXX     XXXXXXXXXX",
"XXXXXXXXXXX P XXXXXXXXXXX",    
"XXXXXXXXXX  X  XXXXXXXXXX",
"XXXXXXXXX  XXX  XXXXXXXXX",
"XXXXXXXX  XXXXX  XXXXXXXX",
"XXXXXXX  XXXXXXX  XXXXXXX",
"XXXXXX  XXXXXXXXX  XXXXXX",
"XXXXX  XXXXXXXXXXX  XXXXX",
"XXXX  XXXXXXXXXXXXX  XXXX",
"XXX  XXXXXXXXXXXXXXX  XXX",
"XXX XXXXXXXXXXXXXXXXX XXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]
level_2 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXP              EX  XXX",
"XXX XXX XXX XXXXX XXX XXX",
"XXX X   X   X   X   X XXX",
"XXX X XXXXX X X XXX X XXX",
"XXX X     X X X   X X XXX",
"XXX XXXXX X X XXX X X XXX",
"XXX     X X X X X X X XXX",
"XXXXX X X X X X X X X XXX",
"XXX   X X X X X X X X XXX",
"XXX XXX X X X X X X X XXX",
"XXX X   X X X X X X X XXX",
"XXX X XXXXX X X X X X XXX",
"XXX X     X X   X X X XXX",
"XXX X XXX X XXXXX X X XXX",
"XXX X X X X     X X X XXX",
"XXX X X X X XXX X X X XXX",
"XXX X X     X   X X X XXX",
"XXX X XXXXX XXXXXX X   XX",
"XXX X     X        X X TX",
"XXX XXXXX XXXXXXXXXX XXXX",
"XXX                   XXX",
"XXX XXXXXXXXXXXXXXXXX XXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]
level_3 =[
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XX     XX  T    XX     XX",
"XX XXX XXXX XXX XXXX X XX",
"XX XXX XX    XX    XX  XX",
"XX XXX XX XX XXXX XXXXXXX",
"XX  E  XX XX     XX    XX",
"XXXX XXXXXXX XXX XXXXX XX",
"XX       XX XXX  X     XX",
"XX XXXXX XX         XXX X",
"XX     X XXXX XXX     X X",
"XXXXX XX      X X X XXXXX",
"XX     XXX XXX     XXX XX",
"XX XXX     XX XXX XXX  XX",
"XX XXX XXX XX XXX   XX XX",
"XX   X XX            EXXX",
"XXX XX XXXX XXXX XX XXXXX",
"XX     XX     XX XX    XX",
"XX XXXXXXX XXXXX XXXXXXXX",
"XX       XX     XX     XX",
"XXXXXXXX  XXXXX XXXXXXX X",
"XX     XX     XX     XX X",
"XX XXX XXXXX XXXXXXX XX X",
"XX   X       P    EXX   X",
"XX XXXXXXXXXXXXXXXXXXX XX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]
treasures = []
enemies = []
levels.append(level_1)
levels.append(level_2)
levels.append(level_3)
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)
            
            if character == "X": #if char == x -> draw wall
                pen.goto(screen_x,screen_y)
                pen.stamp()
                #add coordinates to the wall list
                walls.append((screen_x,screen_y))
                
            elif character == "P": #if char == p -> draw player
                player.goto(screen_x, screen_y)
            
            elif character == "T": #if char == t -> draw treasure
                treasures.append(Treasure(screen_x,screen_y))
            elif character == "E": #if char == e -> draw enemy
                enemies.append(Enemy(screen_x, screen_y))


#create class instances
pen = Pen()
player = Player()

#create walls coordinates
walls = []

#setup the level
setup_maze(levels[current_level_index])

for enemy in enemies: # make a delay of each new enemy spawned so that they don't move at the same time
    turtle.ontimer(enemy.move, t=250)
#Keyboard binds
turtle.listen() # listen for user's input
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")

#turn off screen updates
window.tracer(0)


#main game loop
while True:
    for treasure in treasures:
        if player.is_collision(treasure):
            # add gold of the treasure to the player
            print("You have promoted to the next level!")
            player.gold += treasure.gold
            print("Player gold: {}".format(player.gold))
            for treasure_ in treasures:
                treasure_.destroy()
            for enemy in enemies:
                enemy.destroy()
            enemies = []
            walls = []
            treasures = []
            if current_level_index+1 < len(levels):
                current_level_index += 1
            else:
                current_level_index = 1
            pen.clearstamps()
            window.update()
            playerdata = {"level_index": current_level_index} # cannot pass a diret number, should type it in dictionary
            save_level_index(playerdata)
            print("Current level index: " + str(current_level_index))
            print("Destroyed all treasures. Remaining:", len(treasures))
            setup_maze(levels[current_level_index])
            for enemy in enemies: # make a delay of each new enemy spawned so that they don't move at the same time
                turtle.ontimer(enemy.move, t=250)

    for enemy in enemies:
        if player.is_collision(enemy):
            for enemy in enemies:
                enemy.destroy()
            enemies = []
            walls = []
            treasures = []
            player.gold -= 100
            setup_maze(levels[current_level_index])
            for enemy in enemies: # make a delay of each new enemy spawned so that they don't move at the same time
                turtle.ontimer(enemy.move, t=250)
    window.update()