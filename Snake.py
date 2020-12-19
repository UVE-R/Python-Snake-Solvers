#Snake Solver using A* Pathfinding

import random
import pygame
import time

#Each box in the window is a cube object
class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(0,255,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface,self.color,( i*dis+1 , j*dis+1 , dis-2 , dis-2 ))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius) 

#Snake class
class snake(object):
    body = []
    #Dictionary to store turns by the snake
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        #Body made up of cube objects 
        self.body.append(self.head)
        #Keeps track of directions moving in
        self.dirnx = 0
        self.dirny = 1
        
    #Decide which direction to move in           
    def go(self,path):
        #Find coordinate difference
        current = path[0]        
        x = self.head.pos[0] - current[0] 
        y = self.head.pos[1] - current[1]        
        
        if x==1 and y==0:
            s.left()
        elif x==-1 and y==0:
            s.right()
        elif x==0 and y==1:
            s.up()
        elif x==0 and y==-1:
            s.down()  
      
    #Maving Right
    def right(self):                    
        self.dirnx = 1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        self.move()
    
    #Moving Left
    def left(self):                    
        self.dirnx = -1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        self.move()
    
    #Moving Up
    def up(self):                    
        self.dirnx = 0
        self.dirny = -1
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        self.move()
    
    #Moving Down
    def down(self):    
        self.dirnx = 0
        self.dirny = 1
        #Set the position of the head to a turn
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        self.move()
        
    #Updating the position of the snake
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()            
        
        #Loop through snake's body positions
        #Get index and cube object in self.body             
        for i,c in enumerate(self.body):
            #Get postion of cube object
            p = c.pos[:]
            if p in self.turns: #If the cube is at the turn position
                turn = self.turns[p] #Get the direction to turn
                c.move(turn[0],turn[1]) #Turn the cube
                
                #Remove the turn once all of the snakw has passsed the cube
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                #When the cube is not turning
                #If the cube is at the edge then make it appear at the opposite edge
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1]) #If off the screen to the left, move to the right-most row on the screen 
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny) #Keeps moving the cube when not turning
     
    #Adding a cube to the back of the tail
    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail.dirnx, tail.dirny
        
        #Checks the direction where the tail of the cube is moving in and adds it to the back of the snake 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
         
        #Adds direction to tail
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    #Draw the snake to the window
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                #True draws eyes
                c.draw(surface,True)
            else:
                c.draw(surface)

#Draw the gridlines
def drawGrid(w, rows, surface):
    sizeBtwn = width // rows
    
    x = 0
    y = 0
    
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        
        #Draw horizontal and vertical line grid
        pygame.draw.line(surface,(255,255,255),(x,0),(x,w))
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y))
        
#Main redraw function
def redrawWindow(surface):
    global rows,width,s,snack
    surface.fill((0,0,0))
    drawGrid(width,rows,surface)
    snack.draw(surface)
    s.draw(surface)
    pygame.display.update()    

#Returns coordinates of a snack with respect to the snake
def randomSnack(row, item):
    #List of snake's body coordinates
    positions = item.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        
        #List of a filtered list, then see if any positions are the same as the current position of the snake
        #Stopping us from putting a snack on top of the snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)
 
#Make a grid for the A* algorithm
def make_grid(snake,rows):
    grid = []
    #Get coordinates of each cube of the snake's body
    obstacles = []
    for k in range(len(snake.body)):
        obstacles.append(snake.body[k].pos)
        
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            if (i,j) in obstacles:
                grid[i].append(1)
            else:
                grid[i].append(0)                                    
    return grid

#Node class for pathfinding
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __hash__(self):
        return hash(self.position)
 
#Return the path to the snack from the head to the snack
def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

#A* pathfinding, will return a path if found
#Or will return None if there is no path or there is too many iterations to find a path
def algorithm(maze,start,end, allow_diagonal_movement = False):
    #Keeps track of iteration count
    x=0
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()               

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        x+=1
        #Return None if there is no path or there is too many iterations to avoid crashing
        if x>10000:
            return None

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.add(current_node)    

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:          
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
    
#Main Loop    
def main():
    
    global width,rows,s,snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((500,500))
    
    #Create snake and snack
    s = snake((0,0,0),(10,10))    
    snack = cube(randomSnack(rows, s),color=(255,0,0))   

    flag = True
    clock = pygame.time.Clock()
    
    #True if shortest path found
    found = False
    
    grid = []
    path = []
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        
        #If the snake is the entire screen
        if len(s.body) == 400:
            print("YOU WIN")
            flag = False
        
        #If snake is on the snack
        if  s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s),color=(255,0,0))
            found = False
        elif not found: #If there is no shortest path then find one
            start = s.head.pos
            end = snack.pos
            #Create a grid
            grid = make_grid(s,rows) 
            #Find shortest path
            path = algorithm(grid,start,end)
            
            #If there is no path or the program is going to crash
            if path == None:
                print("No Path Avaliable, or too many iterations")
                flag = False
                break            
            found = True
            try:
                path.pop(0)
            except Exception:
                print("Lose")
                break
        else:#If a path has been found, then go to it
            s.go(path)
            path.pop(0)
          
        #Check to see if position of each body object has the same position of another body object (i.e. It has collided)
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos,s.body[x+1:])):
                print("Lose")
                flag = False
                break
                
        redrawWindow(win)
        
    print("Score is: ", len(s.body))
    time.sleep(3)
    pygame.quit()
    

main()
