#Snake Solver using a Hamiltonian Cycle
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 6
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
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
        
        if current == 1:
            s.up()
        elif current == 2:
            s.right()
        elif current ==3:
            s.down()
        elif current == 4:
            s.left()
      
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
            #print(p)
            #print(self.turns)
        
            if p in self.turns: #If the cube is at the turn position                
                turn = self.turns[p] #Get the direction to turn
                c.move(turn[0],turn[1]) #Turn the cube                
                #Remove the turn once all of the snakw has passsed the cube
                if i == len(self.body)-1:
                    self.turns.pop(p)                   

            else:
                c.move(c.dirnx,c.dirny) #Keeps moving the cube when not turning
    
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

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
        

    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                #True draws eyes
                c.draw(surface,True)
            else:
                c.draw(surface)


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
        

def redrawWindow(surface):
    global rows,width,s,snack
    pygame.display.set_caption("Hamiltonian Cycle Solver")
    surface.fill((0,0,0))
    drawGrid(width,rows,surface)
    snack.draw(surface)
    s.draw(surface)
    pygame.display.update()    

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

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def endScreen(winorlose):
    print("Score: " , len(s.body))
    message_box(winorlose,"Play Again...")
    s.reset((startx,starty))       

def main():
    global width,rows,s,snack, startx, starty
    width = 500
    rows = 6
    startx = 0
    starty = 0
    
    win = pygame.display.set_mode((500,500))
    s = snake((255,0,0),(startx,starty))
    snack = cube(randomSnack(rows, s),color=(0,255,0))
    
    #Path for hamiltonain cycle, 1 is up, 2 is right, 3 is down, 4 is left
    cycle = [3,3,3,3,3,2,1,1,1,1,2,3,3,3,3,2,1,1,1,1,2,3,3,3,3,2,1,1,1,1,1,4,4,4,4,4]   
        
    flag = True
    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(1000)   
        
        if len(cycle) == 0:
            cycle = [3,3,3,3,3,2,1,1,1,1,2,3,3,3,3,2,1,1,1,1,2,3,3,3,3,2,1,1,1,1,1,4,4,4,4,4]
        
        s.go(cycle)
        cycle.pop(0)
    
        if len(s.body) == (rows**2) -1:
            endScreen("You Win")
            cycle = [3,3,3,3,3,2,1,1,1,1,2,3,3,3,3,2,1,1,1,1,2,3,3,3,3,2,1,1,1,1,1,4,4,4,4,4]
        
        if  s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s),color=(0,255,0))
          
        #Check to see if position of each body object has the same position of another body object (i.e. It has collided)
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos,s.body[x+1:])):
                endScreen("You Lose")
                break               

        redrawWindow(win)       
        
main()
