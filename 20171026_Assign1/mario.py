
from person import Person
from bullet import myBullet
from enemies import Boss
class Mario(Person):
    def __init__(self, level):
        Person.__init__(self, 100, 16, 0, (2, 2), [
                        ['o', 'o'], [']', '[']], "Mario")
        self._BulletList = []        #Bullets shot by Mario

    def BigMario(self):
        """Conversion to Big Mario using Mushroom"""
        self._disp = [['{', 'O', 'O', '}'], [']', ']', '[', '[']]
        self._dim = (2, 4)
        self._typ = "BigMario"
        self._jump_dist = 6

    def revert(self,boardA):
        """Losing the powerup"""
        self.clear(boardA)
        self._disp = [['o', 'o'], [']', '[']]
        self._dim = (2,2)
        self._typ = "Mario"
        self._jump_dist = 3

        self.render(boardA)
    
    def clear(self,boardA):
        """Clear the remains of Big Mario while turning small"""
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                boardA.change(self._x+i, self._y+j,'.')

    def shoot(self):
        """Create a bullet"""
        self._BulletList.append(myBullet(self._x, self._y+self._dim[1]))


    def bullet_render(self, bossA, boardA):
        """Render all bullets on board"""
        for bullet in self._BulletList:
            bullet.collision(boardA)
            if bullet.isalive():
                bullet.move(boardA)
                bullet.collision(boardA)
                bullet.render(boardA)
                bullet.kill(bossA,boardA)

    def dead(self,boardA): 
        """Losing life to enemy"""
        if(self._typ == "BigMario"):
            self.revert(boardA)
            return
        self._lives -= 1
        if(not self._lives):
            self.deadf()