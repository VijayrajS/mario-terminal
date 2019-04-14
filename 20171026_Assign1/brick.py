import board
from mario import *

class Brick(object):
    """Defining Bricks."""

    def __init__(self, x, y, length, width, mat = [['#','#'],['#','#']]):
        """Initializing bricks."""
        self._dim = (length, width)
        self._disp = mat
        self._x = x
        self._y = y
        self._destroyed = False
        
    def render(self, boardA):
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                boardA.change(self._x+i, self._y+j,self._disp[i][j])


class Breakable(Brick):
    """Destroyable bricks"""
    def __init__(self, x, y, content):
        Brick.__init__(self, x, y, 2, 2, [['?', '?'], ['?', '?']])
        self._content = content                                        # 1 for Mushroom, 2 for coin
        self._stay = 5

    def destroy(self, boardA, marioP):
        """Destroying the brick."""
        if self._destroyed is False:
            boardA.score_setter(20)
            self._destroyed = True
    
        if(self._stay):
            if(self._content == 1):
                self._disp = [['M', 'M'],['M', 'M']]    #Mushroom
                
                if(self._stay == 5):  
                     marioP.BigMario()
            else:
                self._disp = [['C', 'C'],['C', 'C']]     #Coins
                if(self._stay == 5):
                    boardA.coin_setter(4)

            self._stay -= 1
        else:
            self._disp = [['.', '.'],['.', '.']]
        super().render(boardA)
    
    def MarioChecker(self, boardA, marioP):
        for element in [(self._x+self._dim[0], self._y +i) for i in range(self._dim[1])]:
            if(boardA.specPoint(element[0],element[1]) in ['o','{','O','}']):
                self.destroy(boardA, marioP)
