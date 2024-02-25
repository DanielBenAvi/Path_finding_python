
from attr import dataclass
import pygame


@dataclass
class My_Button:
    '''
    A class to represent a button.
    
    Attributes
    ----------
    text: str
        The text to display on the button.
    x: int
        The x coordinate of the button.
    y: int
        The y coordinate of the button.
    width: int
        The width of the button.
    height: int
        The height of the button.
    callback: function
        The function to call when the button is clicked.
        '''
    text: str
    x: int
    y: int
    width: int
    height: int
    callback = None
    
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.x + 5, self.y + 5))
        
    def is_mouse_over(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            return True
        else:
            return False
        
    def on_click(self):
        if self.callback:
            print("Button clicked - invoking callback function.")
            self.callback()
            
    def set_callback(self, callback):
        self.callback = callback
        return self.callback