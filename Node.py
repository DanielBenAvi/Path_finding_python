from attr import dataclass

@dataclass
class Node:

    x: int
    y: int
    parent = None


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
    


   
        
    