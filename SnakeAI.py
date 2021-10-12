import neat
import random
import pygame
import os

gen = 0
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans",50)

class cube(object):
    rows = 15
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

class Snake(object):
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)

        #Keeps track of directions moving in
        self.dirnx = 0
        self.dirny = 1     
        self.body = []
        self.turns = {}
        #Body made up of cube objects 
        self.body.append(self.head)
      
    def collide(self):
        #Check to see if position of each body object has the same position of another body object (i.e. It has collided)
        for k in range(len(self.body)):
            if self.body[k].pos in list(map(lambda z: z.pos,self.body[k+1:])):
                return True
        return False
    
    def left(self):
        if self.head.dirnx == 1 and len(self.body)>1:
            return True                    
        self.dirnx = -1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        return False
    
    def right(self):
        if self.head.dirnx==-1 and len(self.body)>1:
            return True                    
        self.dirnx = 1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        return False
    
    def up(self):
        if self.head.dirny==1 and len(self.body)>1:
            return True                   
        self.dirnx = 0
        self.dirny = -1
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        return False
    
    def down(self):
        if self.head.dirny==-1 and len(self.body)>1:
            return True                 
        self.dirnx = 0
        self.dirny = 1
        #Set the position of the head to a turn
        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        return False

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
        
def redrawWindow(surface,gen,snakes):
    global rows,width,snack
    pygame.display.set_caption("NEAT Solver")
    surface.fill((0,0,0))
    drawGrid(width,rows,surface)
    snack.draw(surface)
    snakes[0].draw(surface)        
    text = STAT_FONT.render("Gen: " + str(gen-1), 1, (255,255,255))
    surface.blit(text, (10, 10))
        
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
            
def main(genomes,config):
    global width,rows,snack,gen    
    width = 500
    rows = 15
    win = pygame.display.set_mode((500,500))
    temp = 0
    
    gen += 1
    
    nets = []
    ge = []
    snakes = []

    #print(genomes)
    
    for x,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake((255,0,0),(10,10)))        
        g.fitness = 0
        ge.append(g)
    
    
    """
    snakes.pop(-1)
    nets.pop(-1)
    ge.pop(-1)
    
    #ge[1].fitness = -10000
    
    snakes.clear()
    snakes.append(Snake((255,0,0),(10,10)))
    """

    snack = cube(randomSnack(rows, snakes[0]),color=(0,255,0))
    
    flag = True
    clock = pygame.time.Clock()
    
    last_move = -1

    
    
    while flag:
        temp += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()
                quit()
                break
            
        pygame.event.get()
        clock.tick(60)
        
        for x,snake in enumerate(snakes):    
            output = nets[x].activate((snake.head.pos[0], snake.head.pos[1], abs(snake.head.pos[0] - snack.pos[0]), abs(snake.head.pos[1] - snack.pos[1])))

            #GET MAXIMUM
            """
            if output[0] > 0.7:
                snakes[x].left()                   
            elif output[1] > 0.7:
                snakes[x].right()
            elif output[2] > 0.7:
                snakes[x].up()
            elif output[3] > 0.7:
                snakes[x].down()
            """
            """
            if x==0:
                print("0: ",snake.body[0].pos)
            else:
                print("1: ",snake.body[0].pos)
            """
            max_val = max(output)
            max_idx = output.index(max_val)
            #print(ge[x].fitness)
            
            if last_move == max_idx:
                ge[x].fitness -= 5

            last_move = max_idx
            

            if max_idx == 0:
                #print("LEFT: ",snake.body[0].pos)
                snake.left()
            elif max_idx == 1:
                #print("RIGHT: ",snake.body[0].pos)
                snake.right()
            elif max_idx == 2:
                #print("UP: ",snake.body[0].pos)
                snake.up()
            else:
                #print("DOWN: ",snake.body[0].pos)
                snake.down()

                    
            rem = []
            
            snake.move()    
            
            if  snake.body[0].pos == snack.pos: 
                snake.addCube()
                ge[x].fitness += 10
                snack = cube(randomSnack(rows, snake),color=(0,255,0))
                temp = 0
                
            if temp>len(snake.body)*100 or snake.head.pos[0] >rows -1 or snake.head.pos[0]<0 or snake.head.pos[1]<0 or snake.head.pos[1]>rows-1:
                rem.append(snake)         
                
            if snake.collide():
                rem.append(snake)
            
        redrawWindow(win, gen, snakes)
             
        for snake in rem:            
            x = snakes.index(snake)
            ge[x].fitness -= 10
            nets.pop(x)
            ge.pop(x)
            snakes.remove(snake)
        
        if len(snakes) == 0:
            flag = False
            break 

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)      
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)
    pygame.quit()
    
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)
