class Board:
    def __init__(self, length, width):
        """Initializing the board."""
        self.length = length
        self.width = width
        self._score = 0
        self._coins = 0
        self._start = 0
        self._counter = 7001
        self._grid = [['.' for i in range(500)] for j in range(length)]

        for i in range(500):
            self._grid[18][i] = '#'
            self._grid[19][i] = '#'

            for i in range(10,450,50):
                for j in range(18,20):
                    for k in range(3):
                        self._grid[j][i+k] = '.'
        for i in range(17):
            self._grid[i][493] = '#'

    def count(self):
        """Used to render timer"""
        return self._counter//10

    def count_decrement(self):
        self._counter -= 1

    def specPoint(self,x1,y1):
        """Returns the specific character at x1,y1"""
        return self._grid[x1][y1]

    def start_getter(self):
        """Getter for the start variable"""
        return self._start

    def score_getter(self):
        """Getter for the score variable"""
        return self._score

    def score_setter(self, inc):
        """Incrementer for the score variable"""
        self._score += inc

    def coin_getter(self):
        """Getter for the coin variable"""
        return self._coins

    def coin_setter(self, inc):
        """Incrementer for the coin variable"""
        self._coins += inc

    def start_setter(self, val):
        """Setter for the start variable"""
        self._start = val

    def printBoard(self):
        """Return the matrix in string format."""
        strBoard = ""

        for row in self._grid:
            strBoard += ''.join(row[self._start:self._start+80]) + '\n'

        strBoard += "SCORE: " + str(self._score) + "\n"
        strBoard += "COINS: " + str(self._coins) + "\n"
        strBoard += "Press 'q' to exit\n"
        return strBoard

    def change(self, x, y, c):
        """Change a particular character on the grid"""
        self._grid[x][y] = c


