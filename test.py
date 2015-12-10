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
    #colors
    data.Red=(255,0,0)
    data.Blue=(0,0,255)
    data.Green=(0,255,0)
    data.Cloud=(135,206,235)
    data.Space=(252, 252, 250)
    data.Black=(0,0,0)
    data.Grey=(84,84,84)
    
init(data)
makeScreen=pygame.display.set_mode( (data.width, data.height))
pygame.display.set_caption('iBasket Term Project')

def drawPitch():    
    pygame.draw.polygon(makeScreen, data.Grey, ((0,data.height),(200,450),(data.width,450),(data.width,data.height)), 0)
    pygame.draw.line(makeScreen, data.Black, (0,data.height), (200,450), 10)
    pygame.draw.line(makeScreen, data.Black, (200,450), (data.width,450), 10)
    pygame.draw.line(makeScreen, data.Black, (500,data.height), (600,450), 10)
    pygame.draw.line(makeScreen, data.Black, (0,data.height), (data.width,data.height), 10)
    pygame.draw.line(makeScreen, data.Black, (0,data.height), (200,450), 60)
    
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
        
