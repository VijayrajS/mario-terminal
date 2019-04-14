from board import Board
from enemies import Boss

class myBullet():
    def __init__(self, x, y):
        self._disp = '*'
        self._x = x
        self._y = y
        self._next = y + 1
        self._live = True       #Bullet exists?
        self._yinit = y

    def render(self, boardA):
        boardA.change(self._x, self._y-1, '.')
        boardA.change(self._x, self._y, self._disp)

    def isalive(self):
        return self._live

    def collision(self,boardA):
        """Bullet hit"""
        next_char = boardA.specPoint(self._x, self._next)
        if boardA.specPoint(self._x, self._next) != '.':
            self._live = False
            boardA.change(self._x, self._y, '.')
            return next_char
    
    def move(self, boardA):
        """Bullet moving forward"""
        self._y = self._next
        self._next = self._y + 1
        self.render(boardA)
        
    
    def kill(self, bossA, boardA):
        """Kill boss"""
        if(self.collision(boardA) in list("()-|")):
            bossA.dead_1(boardA)
