'''
Created on Nov 26, 2015

@author: rbasomin
'''

import pygame
import sys
from pygame.locals import *
import random
import math


def init(data):
    data.balls=[]
    data.height=700
    data.width=900
    data.level=1   
    data.shootedBalls=0
    data.accuracy=0   
    data.dy=2   #delta y while bouncing
    data.score=0
    data.timer=20
    data.mode="start" #or level or level 1
    #colors
    data.Red=(255,0,0)
    data.Blue=(0,0,255)
    data.Green=(0,255,0)
    data.Cloud=(135,206,235)
    data.Space=(252, 252, 250)
    data.Black=(0,0,0)
    data.Grey=(84,84,84)
    data.Yellow=(255,255,0)
    data.white=(255,255,255)
    #basket
    data.basketW=50 #width
    data.heightH=40 #height
    data.basketX0=176#169
    data.basketY0=265 #273
    data.basketX1=250#250
    data.basketY1=280   
    #pitch measure
    data.pitchHeight=450
    data.pitchMargin=200

#all pygame modules declared are initialized
pygame.init()

#adapted song by Lil Jon-Snap your finger
ballSound = 'sounds/snapFinger.mp3'
pygame.mixer.init()
pygame.mixer.music.load(ballSound)
pygame.mixer.music.play()

class Struct(object): pass
data = Struct()
init(data)
makeScreen=pygame.display.set_mode( (data.width, data.height))
pygame.display.set_caption('iBasket Term Project')


#class drawing the ball
class Ball(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.bend=1
        self.jump=10
        
        self.destX=0
        self.destY=0
        self.r=20   #radius
        self.move=False
        self.bounce=False
        self.bounceDirection="up"
        self.bounceLimit=data.height//2
        self.movingDirection="straight" #or up or down
        self.movingRight=False
        self.bending=False
    
    def destinations(self,x,y):
        pass
           
    def drawBall(self):            
        #Fake shadow
        if self.y<(data.height//2):
            self.yb=5*data.height//7
        else:
            self.yb=self.y+((data.height-self.y)//2)                    
        pygame.draw.circle(makeScreen, data.Black, 
                           (self.x+10,self.yb), self.r, 0)     
        #the ball
        pygame.draw.circle(makeScreen, data.Red, (self.x,self.y), self.r, 0)
        
    def hitBasket(self):
        if((data.height//7<self.x<150 and 2*(data.height//7)<self.y<3*(data.height//7)) or (90<self.x<110 and 300<self.y<550)):
            #print("1st Hit")
            return [True,"down"]
        elif(((self.y>data.basketY0 and self.y<data.basketY1) and (176>self.x and self.x>146)) or 
             ((self.y>data.basketY0 and self.y<data.basketY1) and (262>self.x and self.x>242))):
            #print("hit")
            return [True,"down"]
        return False
    
    def ifScored(self):
        
        if((self.y>data.basketY0+10 and self.y<data.basketY1) and (data.basketX1>self.x and self.x>data.basketX0)):
            #ball.movingDirection="straight"
            return True
        return False
        
    def moveBall(self):
        #formula math.cos(self.angle) * self.speed
        #adapted from http://goo.gl/u7lOKs                
        if(self.ifScored() and self.movingDirection=="down"): 
            #self.movingDirection=="down"):
            data.score+=50
            
        elif(self.ifScored() and self.movingDirection=="up"):
            self.movingDirection="down"
            self.bending=True
        
        #if ball hit the basket
        if(self.hitBasket()):
            self.movingRight=True
            #print("dire",self.hitBasket()[1])
            self.movingDirection=self.hitBasket()[1]
            self.bounce=False
            self.bending=True

        if(self.movingDirection=="straight"):
            if(self.x-(self.r*2) <= self.destX and self.x+(self.r*2)> self.destX):
                if(self.y>=9*data.height//10):
                    self.move=False
                    self.bounce=True
                if(not self.bending):
                    self.x =self.x
                    self.y -= int(math.cos(self.bend) * self.jump)
                    if(self.y<=self.destY):
                        self.bending=True
                else:
                    self.x =self.x
                    self.y += int(math.cos(self.bend) * self.jump)
            elif(self.y-(self.r*2) <= self.destY and self.y+(self.r*2)> self.destY):
                if(self.x-(self.r*2) <= self.destX):
                    self.y =self.y
                    self.x += int(math.cos(self.bend) * self.jump)
                else:
                    self.y =self.y
                    self.x -= int(math.cos(self.bend) * self.jump)
                    
        elif(self.movingDirection=="up"):           
            self.destX=self.destX
            self.destY=self.destY
            if(self.y>=9*data.height//10):
                self.move=False
                self.bounce=True
                         
            if(self.destX>self.x+self.r):
                if self.destY>self.x:
                    self.x += int(math.sin(self.bend) * self.jump)
                    self.y += int(math.cos(self.bend) * self.jump)
                else:
                    self.x += int(math.sin(self.bend) * self.jump)
                    self.y -= int(math.cos(self.bend) * self.jump)
                    
            elif(self.destX<self.x-self.r):
                if self.destY>self.x:
                    self.x -= int(math.sin(self.bend) * self.jump)
                    self.y += int(math.cos(self.bend) * self.jump)
                else:
                    self.x -= int(math.sin(self.bend) * self.jump)
                    self.y -= int(math.cos(self.bend) * self.jump)
            else:
                self.movingDirection="down"
                self.bending=True
                self.x -= int(math.sin(self.bend) * self.jump)#self.destX
                self.y += int(math.cos(self.bend) * self.jump)
    
        elif(self.movingDirection=="down"):
            if(not self.movingRight):
                self.x -= int(math.sin(self.bend) * self.jump)#self.destX
                self.y += int(math.cos(self.bend) * self.jump)
                if(self.y>=9*data.height//10):
                    self.bounce=True
            else:
                self.x += int(math.sin(self.bend) * self.jump)#self.destX
                self.y += int(math.cos(self.bend) * self.jump)
                if(self.y>=9*data.height//10):
                    self.bounce=True
            
    def bounceBall(self):
        if(self.bounceDirection=="up"):
            if(data.height-self.bounceLimit>data.height-self.y):
                self.y-=data.dy
            elif(data.height-self.bounceLimit<=data.height-self.y):
                self.bounceLimit+=(((9*data.height//10)-self.bounceLimit)//2)
                self.bounceDirection="down"
        else:
            if(self.y<9*data.height//10):
                self.y+=data.dy
            else:
                self.bounceDirection="up"
                if(self.y-self.bounceLimit<3):
                    self.bounce=False
                    #self.kill()   

class Clouds(object):  # represents the cloud and move it
    def __init__(self,x,y):
        self.x1=x
        self.x0=40
        self.y=y
        
    def drawClouds(self,makeScreen):
        #draw the clouds        
        x1=self.x1
        pygame.draw.circle(makeScreen, data.Cloud, 
                           (x1+self.x0,(self.y)+self.x0), 3*self.x0//4)
        pygame.draw.circle(makeScreen, data.Cloud, 
                           (x1+(self.x0//2),(self.y)+3*self.x0//2), 
                           3*self.x0//5)
        pygame.draw.circle(makeScreen, data.Cloud, 
                           (x1+(self.x0*3//2),(self.y)+3*self.x0//2), 
                           3*self.x0//5)
        
    def moveCloud(self):
        if((self.x1+(self.x0*3//2))>0):
            self.x1-=1
        else: self.x1=data.width
        
class Basket(object):
    def __init__(self):
        #to do
        #try to use sprite to detect collision
        pygame.sprite.Sprite.__init__(self)
    def drawBasket(self):
        pygame.draw.line(makeScreen, data.Black, (100,550), 
                         (100,300), 30)
        pygame.draw.polygon(makeScreen, data.Blue, ((70,330),
                        (150,300),(150,200),(70,230)), 0)
        pygame.draw.line(makeScreen, data.Black, (100,280), 
                         (150,280), 18)
        
    def finalBasket(self):
        basket = pygame.image.load('image/basket.png')
        makeScreen.blit(basket,(150,250))
        
    def halfFinalBasket(self):
        basket = pygame.image.load('image/basket2.png')
        makeScreen.blit(basket,(150,250))


def drawPitch():
    #draw the pitch with a grey color filled in
    pygame.draw.polygon(makeScreen, data.Grey, 
                    ((0,data.height),(data.pitchMargin,data.pitchHeight),
                    (data.width,data.pitchHeight),(data.width,data.height)),0)
    pygame.draw.line(makeScreen, data.Black, (0,data.height), 
                     (data.pitchMargin,data.pitchHeight), 10)
    pygame.draw.line(makeScreen, data.Black, 
                     (data.pitchMargin,data.pitchHeight), 
                     (data.width,data.pitchHeight), 10)
    pygame.draw.line(makeScreen, data.Black, 
                     (data.pitchHeight+data.pitchMargin//2,data.height), 
                     ((data.pitchMargin+data.pitchHeight),data.pitchHeight), 
                     10)
    pygame.draw.line(makeScreen, data.Black, (0,data.height), 
                     (data.width,data.height), 10)
    pygame.draw.line(makeScreen, data.Black, (0,data.height), 
                     (data.pitchMargin,data.pitchHeight), 60)
    
def drawWall(data):
    #image from http://goo.gl/nqvwrF
    backG = pygame.image.load('image/tile.png') 
    wall = backG.get_rect()
    width=wall.width
    height=wall.height
    for x in range(0,data.width,width):
        for y in range(2*data.height//5,4*data.height//7,height):
            makeScreen.blit(backG,(x,y))
    #image from http://goo.gl/3sZ2NW   
    Gazon = pygame.image.load('image/gazon.jpg') 
    gazonSize = Gazon.get_rect()
    width=gazonSize.width
    height=gazonSize.height
    for x in range(0,data.width,width):
        for y in range(4*data.height//7,data.height,height):
            makeScreen.blit(Gazon,(x,y))  
    
def updateScore():
    myfont = pygame.font.SysFont("Times New Roman", 70,bold=True)
    label = myfont.render("Score:"+str(data.score), 1, data.Blue)
    data.accuracy=round((data.score/(data.shootedBalls*50)*100)if data.shootedBalls>0 else 0,2)
    label1=myfont.render("Accuracy:"+str(data.accuracy)+"%", 1, data.Blue)
    makeScreen.blit(label, (250, data.height//4))
    makeScreen.blit(label1, (250, data.height//7))
    
def updateTimer():
    myfont = pygame.font.SysFont("Times New Roman", 60,bold=True)
    label = myfont.render("Time:"+str(data.timer), 1, data.Yellow)
    makeScreen.blit(label, (2*data.width//3, 3*data.height//7)) 
    
           
def startScreen():
    myfont = pygame.font.SysFont("Times New Roman", 45,bold=True)
    label = myfont.render("Welcome to iBasket game", 1, data.Blue)
    label1 = myfont.render("Just relax and press S to start", 1, data.Yellow)
    label2 = myfont.render("Press H for instructions", 1, data.Green)
    makeScreen.blit(label, (50, 150))
    makeScreen.blit(label1, (50, 250))
    makeScreen.blit(label2, (50, 350))
    
def helpScreen():
    makeScreen.fill(data.white)
    myfont = pygame.font.SysFont("Times New Roman", 35,bold=True)
    label = myfont.render("Welcome to iBasket game.    Press S to start playing!", 1, data.Black)
    label1=myfont.render(
'''Welcome         to iBasket game.\n    
Press S to start \t aying!''',
                         1, (255,255,0))
    makeScreen.blit(label, (50, 150))
    makeScreen.blit(label1,(50,200))

    
def drawScore():
    myfont = pygame.font.SysFont("Times New Roman", 80,bold=True)
    label = myfont.render("This is iBasket game", 1, data.Blue)
    label1 = myfont.render("You scored:"+str(data.score), 1, data.Blue)
    label2=myfont.render("Accuracy:"+str(data.accuracy)+"%", 1, data.Yellow)
    label3 = myfont.render("Press r to play level 2", 1, 
                            data.Green)if (data.score>500 and 
                            data.accuracy>50) else myfont.render(
                            "Press r to restart", 1, data.Green)
    makeScreen.blit(label, (150, 100))
    makeScreen.blit(label1, (150, 160))
    makeScreen.blit(label2, (150, 270))
    makeScreen.blit(label3, (150, 325))
    
# create clouds' instances
P = Clouds(data.width,(random.randint(0,150)))
R = Clouds(750,(random.randint(10,150)))
O = Clouds(500,(random.randint(10,150)))
J = Clouds(600,(random.randint(10,150)))
E = Clouds(450,(random.randint(10,150)))
C = Clouds(300,(random.randint(10,150)))
T = Clouds(150,(random.randint(10,150)))
 
#create ball instances
#ball=Ball((random.randint(300,600)),(random.randint(300,500)))

basket=Basket()

#to do
#sprite to deal with collision
#sBasket=pygame.sprite.Group
#sBall=pygame.sprite.Group
#sBasket.add(basket)
#sBall.add(ball)

clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT+1, 1000)

#convert string to class instances
def str2Class(s):
    if s in globals() and isinstance(Clouds, type):
            return globals()[s]
    return None

###########################################################
###   Run the l0op below till the application exit    ####
###########################################################
while True:
    pygame.display.update() # update the screen
    clock.tick(50)
    ######################  ####################
    ###    The first start screen           ####
    ######################  ####################
    if(data.mode=="start"):
        
        startScreen()
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    ##ball=Ball((random.randint(400,700)),(random.randint(300,320)))
                    data.balls.append(Ball((random.randint(400,700)),(random.randint(300,320))))
                    data.mode="level1"
                elif event.key==K_h:
                    data.mode="help"
                    
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
    #######################################################
    ##################### First level #####################
    #######################################################
    elif(data.mode=="level1"):
        makeScreen.fill(data.Space) #fill with the space color
        for i in "PROJECT":
            i=str2Class(i) #convert to class instance
            i.moveCloud()
            i.drawClouds(makeScreen)
            
        #display the wall on the side of the pitch
        drawWall(data)   
        #draw the pitch      
        updateScore()
        updateTimer()        
        drawPitch()    
        #draw ball            
        basket.drawBasket()        
        basket.finalBasket()
        for ball in data.balls:
            ball.drawBall()        
               
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == USEREVENT+1:
                data.timer -= 1
                if(data.timer==0):
                    data.mode="score"
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            if  event.type ==pygame.MOUSEBUTTONUP:
                #print(pygame.mouse.get_pos())
                ball.destX=pygame.mouse.get_pos()[0]
                ball.destY=pygame.mouse.get_pos()[1]
                ball.move=True
                ball.bounceLimit=data.height-((data.height-ball.destY)//3)
                data.shootedBalls+=1
                data.balls.append(Ball((random.randint(400,700)),(random.randint(300,320))))

        basket.halfFinalBasket() 
        #for a in s
        for ball in data.balls:
            if(ball.move):
                if(ball.movingDirection=="straight" and 
                                        ((ball.x-(ball.r*2) <= ball.destX and
                                                ball.x+(ball.r*2)> ball.destX) or 
                                                (ball.y-(ball.r*2) <= ball.destY and 
                                                 ball.y+(ball.r*2)> ball.destY))):
                    ball.movingDirection="straight"
                    ball.moveBall()
                elif(ball.destY<ball.y):                
                    if(not ball.bending):
                        if(ball.destX<ball.x):
                            ball.movingRight=False
                        else:
                            ball.movingRight=True                       
                        ball.movingDirection="up"
                    ball.moveBall()
                else:
                    ball.movingDirection="down"
                    ball.moveBall()            
            if(ball.bounce):
                ball.bounceBall()
                
    #######################################################
    ##################### Second level ####################
    #######################################################
    elif(data.mode=="level2"):
        makeScreen.fill(data.Space) #fill with the space color
        for i in "PROJECT":
            i=str2Class(i) #convert to class instance
            i.moveCloud()
            i.drawClouds(makeScreen)
            
        #display the wall on the side of the pitch
        drawWall(data)   
        #draw the pitch      
        updateScore()
        updateTimer()        
        drawPitch()    
        #draw ball            
        basket.drawBasket()        
        basket.finalBasket()
        ball.drawBall()        
               
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == USEREVENT+1:
                data.timer -= 1
                if(data.timer==0):
                    data.mode="score"
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:                
                if event.key == K_s:
                    ball=Ball((random.randint(400,800)),
                              (random.randint(300,500)))
                    #init(data)
                    ball.move=False
                    ball.bounce=False
                    ball.bounceDirection="up"
                    ball.movingDirection="straight" #or up or down
                    ball.movingRight=False
                    ball.bending=False
                    data.shootedBalls+=1

            if  event.type ==pygame.MOUSEBUTTONUP:
                #print(pygame.mouse.get_pos())
                ball.destX=pygame.mouse.get_pos()[0]
                ball.destY=pygame.mouse.get_pos()[1]
                ball.move=True
                ball.bounceLimit=data.height-((data.height-ball.destY)//3)

        basket.halfFinalBasket() 
        if(ball.move):
            if(ball.movingDirection=="straight" and 
                                    ((ball.x-(ball.r*2) <= ball.destX and
                                            ball.x+(ball.r*2)> ball.destX) or 
                                            (ball.y-(ball.r*2) <= ball.destY and 
                                             ball.y+(ball.r*2)> ball.destY))):
                ball.movingDirection="straight"
                ball.moveBall()
            elif(ball.destY<ball.y):                
                if(not ball.bending):
                    if(ball.destX<ball.x):
                        ball.movingRight=False
                    else:
                        ball.movingRight=True                       
                    ball.movingDirection="up"
                ball.moveBall()
            else:
                ball.movingDirection="down"
                ball.moveBall()            
        if(ball.bounce):
            ball.bounceBall()
            
    ######################################################################
    ############# Score mode, to display score once the game finished#####
    ######################################################################
    elif(data.mode=="score"):
        makeScreen.fill(data.Space) #fill with the space color
        for i in "PROJECT":
            i=str2Class(i) #convert to class instance
            i.moveCloud()
            i.drawClouds(makeScreen)            
        #display the wall 
        drawWall(data)        
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    tempScore=data.score
                    tempAccuracy=data.accuracy
                    init(data)
                    data.balls.append(Ball((random.randint(400,700)),(random.randint(300,320))))
                    data.mode="level2" if(tempScore>500 and tempAccuracy>50) else "level1"
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        drawScore()
    elif(data.mode=="help"):
        helpScreen()
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    init(data)
                    data.mode="level1"
            if event.type==QUIT:
                pygame.quit()
                sys.exit() 
