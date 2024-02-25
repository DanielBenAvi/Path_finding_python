from attr import dataclass
import pygame

from const import BORDER_COLOR, NODE_SIZE

@dataclass
class Node:

    x: int
    y: int
    parent = None
    h: int = 0


    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent


    def set_parent(self, parent):
        self.parent = parent
        return self.parent
    
    def get_parent(self):
        return self.parent
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def claculate_h(self, x, y):
        self.h = abs(x - self.x) + abs(y - self.y)
        return self.h
    
    def __it__(self, other):
        return self.h < other.h

    def draw_h(self, screen):
        font = pygame.font.Font(None, 16)
        text = font.render(str(self.h), True, BORDER_COLOR)
        screen.blit(text, (self.x * NODE_SIZE + 5, self.y * NODE_SIZE + 5))

   
        
    