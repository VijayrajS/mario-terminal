import sys
import os
import time
import board
from input import input_to, Get
from brick import *
from colorama import Fore, Style

class Person:
    """disp : array of characters making up the playable hero/enemy
       (x,y): Top left coordinates
       dim  : Tuple stating dimensions of the Person on board
       typ  : Type of charcter
       isalive, lives : Name makes variable's use intuitive
       jump_flag : This flag is used to limit the jumping of the character to one jump at a time 
       jump_dist : Vertical coordinate difference between first and highest point of jump"""

    def __init__(self,l, x, y, dim, disp, typ):
        self._x = x
        self._y = y
        self._disp = disp
        self._dim = dim
        self._typ = typ
        self._lives = l
        self._isalive = True
        self._jump_flag = 0
        self._jump_dist = 3

    def debug(self, boardA):
        """Debug statement"""
        print(
            ' '.join([str(self._x), str(self._y), str(self._lives), '\n']))

    def healthcheck(self):
        u = '█'*(self._lives//5) + ' '
        if self._lives >70:
            print(Fore.GREEN + u + str(self._lives) + Style.RESET_ALL)
        elif self._lives <=70 and self._lives >30:
            print(Fore.YELLOW +u +str(self._lives) + Style.RESET_ALL)
        else:
            print(Fore.RED + u +str(self._lives)+ Style.RESET_ALL)

    def getLive(self):
        """Getter for alive status"""
        return self._isalive
    
    def xyGetter(self):
        """Getter for xy coordinates"""
        return (self._x, self._y)

    def dimGetter(self):
        """Getter for dimensions"""
        return self._dim

    def move(self, chbuff, boardA, en=None, br = None):
        checker_l = self.col_check(boardA)
        if chbuff == 'd' and self._y < 500 - self._dim[1]:
            """Right"""
            if len(checker_l):
                for checker in checker_l:
                    if(checker[1] == self._y + self._dim[1]):
                        return

            self._y += 1
            for i in range(self._dim[0]):
                boardA.change(self._x+i, self._y-1, '.')

            if(self._y >= boardA.start_getter() + 40 and self._y < 460 and self._typ != "Enemy"):
                boardA.start_setter(boardA.start_getter()+1)

            self.render(boardA)

        elif chbuff == 'a' and self._y:
            """Left"""
            if len(checker_l):
                for checker in checker_l:
                    if(checker[1] == self._y - 1):
                        return

            if(self._y > 0):
                self._y -= 1

                for i in range(self._dim[0]):
                    boardA.change(self._x+i, self._y+self._dim[1], '.')

                if(self._y < boardA.start_getter() and self._typ != "Enemy"):
                    boardA.start_setter(boardA.start_getter()-1)

                self.render(boardA)

            else:
                pass

        elif chbuff == 'w' and self._jump_flag == 0:
            """Jump up"""
            temp = self._x
            self._jump_flag = 1

            for checker in checker_l:
                if(checker[0] == self._x - 1):
                    self.render(boardA)
                    return
            
            while(self._x and self._x >= temp - self._jump_dist):
                
                if len(checker_l):
                    for checker in checker_l:
                        if(checker[0] == self._x - 1):
                            return
                self._x -= 1
                

                for wi in range(self._dim[1]):
                    boardA.change(self._x+self._dim[0], self._y+wi, '.')
                self.render(boardA)
                checker_l = self.col_check(boardA)
                

                getch = Get()
                chbuff = input_to(getch)

                if(chbuff):
                    self.move(chbuff, boardA)

                if(en):
                    for e in en:
                        e.graze(boardA)
                        e.render(boardA)


                self.render(boardA)
                os.system('clear')
                print(boardA.printBoard())
                print(boardA.count())
        self.render(boardA)

    def gravity(self, boardA, en=None):
        """Bring Mario down if the ground is empty below him"""
        try:
            while(not(self.ground_check(boardA))):

                self._x += 1

                for wi in range(self._dim[1]):
                    boardA.change(self._x-1, self._y+wi, '.')

                getch = Get()
                chbuff = input_to(getch)
                  
                if(chbuff):
                    self.move(chbuff, boardA)

                if(en):
                    for e in en:
                        e.graze(boardA)
                        e.render(boardA)

                self.render(boardA)
                os.system('clear')

                print(boardA.printBoard())
                print(boardA.count())

            self._jump_flag = 0
        
        except: 
           self.deadf()
           return

    def dead(self,boardA): 
        """Losing life to enemy"""
        self._lives -= 1
        if(not self._lives):
            self.deadf()

    def deadf(self):
        """Final Death, or falling in ditch"""
        self._isalive = False
        self._disp = [['.' for _ in range(self._dim[0])] for k in range(self._dim[1])]

    def col_check(self, boardA):
        """Collison checker (Returns collison coordinates)"""
        coords = [*([(self._x-1, self._y+i) for i in range(self._dim[1])]
                    +[(self._x+i, self._y-1) for i in range(self._dim[0])]
                    +[(self._x+i, self._y+self._dim[1])
                       for i in range(self._dim[0])]
                    )]
        
        clash_list = []
        dang_chars = ['0','A']        #Enemy characters
        if(self._typ in ["Mario","BigMario"]):
            dang_chars += list("()-|")
        flag = 1

        for coord in coords:
            if(boardA.specPoint(coord[0], coord[1]) != '.'):
                if(boardA.specPoint(coord[0], coord[1]) in dang_chars and flag):
                    flag = 0
                    self.dead(boardA)
                clash_list.append(coord)

        return clash_list

    def ground_check(self, boardA):
        """Checking for ground/obstacles below"""
        coords = [*([(self._x+self._dim[0], self._y+i) 
                  for i in range(self._dim[1])])]
        for coord in coords:
            if(boardA.specPoint(coord[0], coord[1]) != '.'):
                return (coord)

        return None

    def render(self, boardA):
        """Places character on screen"""
        try:
            for i in range(self._dim[0]):
                for j in range(self._dim[1]):
                    boardA.change(self._x+i, self._y+j, self._disp[i][j])
        except IndexError:
            print(str(i) + ' ' +str(j))
