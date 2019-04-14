from board import Board
from person import Person

class Enemy(Person):
    def __init__(self, x, y, level):
        Person.__init__(self,1, x, y, (2, 2), 
                        [['0', '0'], ['A', 'A']], "Enemy")
        self._speed = level if level < 3 else 2
        self._coor = 0
        self._dirflag = 1  # 1 for ->, 0 for <-

    def graze(self, boardA):
        """Oscilations of enemy"""
        coll_vec = self.col_check(boardA)
        side_col_vec_l = [p for p in coll_vec if p[1] == self._y - 1] #left side collision vector
        side_col_vec_r = [p for p in coll_vec if p[1] == self._y + self._dim[1]] #right side collision vector

        if(self._dirflag == 1):
            self.move('d', boardA)
            self._coor += self._speed
            if(self._coor == 10 or side_col_vec_r):
                self._dirflag = 0

        if(self._dirflag == 0):
            self.move('a', boardA)
            self._coor -= self._speed
            if(self._coor == 0 or side_col_vec_l):
                self._dirflag = 1
    
    def MarioChecker(self, boardA):
        """Check for mario from above"""
        for element in [(self._x-1, self._y +i) for i in range(self._dim[1])]:
            if(boardA.specPoint(element[0],element[1]) in [']','[']):
                boardA.score_setter(100)
                self.deadf()

class Boss(Enemy):
    def __init__(self, x, y, mP):
        Person.__init__(self, 100, x, y,(5,5),
                        [['.','(','0',')','.'],
                         ['-','-','-','-','-'],
                         ['-','-','-','-','-'],
                         ['|','.','|','.','|'],
                         ['|','.','|','.','|']], 
                         "Enemy"
                        )
        self._speed = 1
        self._follow = mP.xyGetter()[1]
        self._activate = 0                   #To activate enemy after mario crosses 425

    def clear(self,boardA):
        """Clear enemy screen"""
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                boardA.change(self._x+i, self._y+j,'.')

    def graze(self, boardA, mP):
        """Mario follower"""
        self._follow = mP.xyGetter()[1]
        if(self._follow >= 425):
            self._activate = 1

        if(self._activate):
            coll_vec = self.col_check(boardA)
            side_col_vec_l = [p for p in coll_vec if p[1] == self._y - 1] #left side collision vector
            side_col_vec_r = [p for p in coll_vec if p[1] == self._y + self._dim[1]] #right side collision vector
            
            self._follow = mP.xyGetter()[1]

            if (self._y > mP.xyGetter()[1]+mP.dimGetter()[1] or self._y>= 493 ) and not len(side_col_vec_l):
                self.clear(boardA)
                self._y -= self._speed
                self.render(boardA)
            elif( mP.xyGetter()[1] > self._y + self._dim[1] or self._y <= 460) and not len(side_col_vec_r):
                self.clear(boardA)
                self._y += self._speed
                self.render(boardA)
    def dead_1(self,boardA):
        """Losing life"""
        if(self._lives<=0):
            self._isalive = False
            self._disp = [['.' for _ in range(self._dim[0])] for k in range(self._dim[1])]
            self.clear(boardA)
            return

        self._lives -= 5

        if(self._lives<=0):
            self._isalive = False
            self._disp = [['.' for _ in range(self._dim[0])] for k in range(self._dim[1])]
            self.clear(boardA)
            return
        