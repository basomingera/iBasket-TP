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
