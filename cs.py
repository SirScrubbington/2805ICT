import random as rand

class colour_square():
    def __init__(self):
        r = rand.randint(0,2)
        if r == 0:
            self.colour = "Red"

        if r == 1:
            self.colour = "Yellow"

        if r == 2:
            self.colour = "Blue"

        self.is_bomb = False
        self.is_flagged = False
        self.is_triggered = False
        self.is_covered = True
        self.adjacent = 0