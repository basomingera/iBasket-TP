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
init(data)
