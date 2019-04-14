
from board import *
from mario import Mario
from enemies import Enemy, Boss
from input import input_to, Get
import os
import sys
from brick import *
from random import randint
from colorama import Fore, Style

b1 = Board(20, 80)

mP = Mario(1)
enList = [Enemy(16, 20, 1),
          Enemy(16, 70, 1),
          Enemy(16, 120, 1),
          Enemy(16, 170, 1),
          Enemy(16, 220, 1),
          Enemy(16, 270, 1),
          Enemy(16, 320, 1),
          Enemy(16, 400, 1)]

brickList = []
breakList = []

brickMap = []
breakMap = []

forbidden_list =  [i+2 for i in range(10,400,50)]
forbidden_list += [i+1 for i in range(10,400,50)]
forbidden_list += [i for i in range(10,400,50)]

# If bricks spawn with y coordinate above, 
# the game would be unplayable
#print(forbidden_list)

def rand_no_gen():
    q = 10
    while(not q%10 or q in forbidden_list):
        q = randint(10,400)
    return q

def random_board_builder():
    for i in range(25):
        t = (14, rand_no_gen())
        
        brickMap.append(t)

        zero_one = [randint(0,2) for _ in range(4)]

        if(zero_one[0]):
            breakMap.append((t[0],t[1]+2))
        if(zero_one[1] and (t[0] - 2,t[1]+2) not in breakMap):
            brickMap.append((t[0] - 2,t[1]+2))
        if(zero_one[2] and zero_one[1]):
             breakMap.append((8, t[1]+3))

    for br_coord in brickMap:
        temp = Brick(br_coord[0], br_coord[1],2,2)
        brickList.append(temp)
    
    mushroom_count = 0

    for br_coord in breakMap:
        
        rand = randint(1,3)

        if(rand == 1 and mushroom_count < 4):
            temp = Breakable(br_coord[0], br_coord[1],1)
            mushroom_count += 1

        else:
            temp = Breakable(br_coord[0], br_coord[1],2)

        breakList.append(temp)


def quit(won,b1):
    os.system('clear')
    print("GAME OVER")
    state = "won!" if won else "lost."
    print("You " + state)
    print("SCORE: " + str(b1.score_getter()))
    print("COINS: " + str(b1.coin_getter()))
    exit()

if __name__ == '__main__':

    random_board_builder()
    print(Fore.BLUE)
    print("___  ___           _        ______             ")  
    print("|   /  |          (_)       | ___ |             ")
    print("| .  . | __ _ _ __ _  ___   | |_/ /_ __ ___ ___ ")
    print("| |VV| |/ _` | '__| |/ _ V  | ___ | '__/ _ V__|")
    print("| |  | | (_| | |  | | (_)|  |_/ / | |   (_)|__ -")
    print("|_|  |_/V__,_|_|  |_|V___/  V____/|_|  |___/|___/")
    print('\nDEVELOPER: VIJAYRAJ SHANMUGARAJ\n\n')
    print("Press any key to get started (D for developer mode/No enemies)")                                     
    print(Style.RESET_ALL)     

    mP.BigMario()                                 
    while(1):
        
        getstart = Get()
        chstart = input_to(getstart)
        
        if(chstart == 'D'):
            enList = []
            break

        if(chstart):
            break
    
    boss1 = Boss(13, 475, mP)
    while mP.getLive() and b1.count():
        getch = Get()
        chbuff = input_to(getch)

        for b in brickList:
            b.render(b1)
        for b in breakList:
            b.MarioChecker(b1,mP)
            b.render(b1)
        
        if chbuff:
            if chbuff or (mP.xyGetter()[1] == 492 - mP.dimGetter()[1] and chbuff!='d'):
                mP.move(chbuff, b1, enList,breakList)
            if chbuff == 'b' and mP.xyGetter()[1] >=400:
                mP.shoot()

        mP.render(b1)
        mP.gravity(b1,enList)
        mP.bullet_render(boss1,b1)

        for i in range(len(enList)):
            if(enList[i].getLive()):
                enList[i].MarioChecker(b1)
                enList[i].render(b1)
                enList[i].graze(b1)
                enList[i].gravity(b1)
        
        
        if boss1.getLive():
            boss1.clear(b1)
            boss1.render(b1)
            boss1.graze(b1,mP)
        
        
        os.system('clear')
        print(b1.printBoard())
        print(b1.count())
        mP.healthcheck()
        print()
        boss1.healthcheck()
        mP.col_check(b1)
        

        b1.count_decrement()

        if chbuff == 'q':
            os.system('clear')
            quit(0,b1)

        if mP.xyGetter()[1] == 492 - mP.dimGetter()[1] and b1.count() and not boss1.getLive():
            quit(1,b1)

    quit(0,b1)
