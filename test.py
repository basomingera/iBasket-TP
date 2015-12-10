'''
Created on Nov 26, 2015

@author: rbasomin
'''

import pygame
import sys
from pygame.locals import *
import random
import math

#all pygame modules declared are initialized
pygame.init()

class Struct(object): pass
data = Struct()

def init(data):
    data.height=700
    data.width=900
    data.level=1
    data.destX=0
    data.destY=0
    data.r=20   #radius
    data.move=False
    data.bounce=False
    data.bounceDirection="up"
    data.bounceLimit=data.height//2
    data.movingDirection="straight" #or up or down
    data.movingRight=False
    data.bending=False
    data.dy=3   #delta y while bouncing
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
    
    #basket sizes
    data.basketW=50 #width
    data.heightH=40 #height
    
    #pitch measure
    data.pitchHeight=450
    data.pitchMargin=200


init(data)
makeScreen=pygame.display.set_mode( (data.width, data.height))
pygame.display.set_caption('iBasket Term Project')

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
        
        
def startScreen():
    myfont = pygame.font.SysFont("monospace", 45,bold=True)
    label = myfont.render("Welcome to iBasket game", 1, (255,255,0))
    label1 = myfont.render("Just relax and press S to start", 1, (255,255,0))
    makeScreen.blit(label, (150, 150))
    makeScreen.blit(label1, (50, 200))
    
# create clouds' instances
P = Clouds(data.width,(random.randint(0,150)))
R = Clouds(750,(random.randint(10,150)))
O = Clouds(500,(random.randint(10,150)))
J = Clouds(600,(random.randint(10,150)))
E = Clouds(450,(random.randint(10,150)))
C = Clouds(300,(random.randint(10,150)))
T = Clouds(150,(random.randint(10,150)))
 
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT+1, 1000)

#convert string to class instances
def str2Class(s):
    if s in globals() and isinstance(Clouds, type):
            return globals()[s]
    return None


while True:
##run till the app exit
    pygame.display.update() # update the screen
    clock.tick(50)
    #start screen
    if(data.mode=="start"):
        
        startScreen()
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    data.mode="level1"
               
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
    #first level
    elif(data.mode=="level1"):
        makeScreen.fill(data.Space) #fill with the space color
        for i in "PROJECT":
            i=str2Class(i) #convert to class instance
            i.moveCloud()
            i.drawClouds(makeScreen)
