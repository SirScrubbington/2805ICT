import random as rand

class colour_square():
    def __init__(self):
        r = rand.randint(0,2)
        if r == 0:
            self.colour = "red"

        if r == 1:
            self.colour = "yellow"

        if r == 2:
            self.colour = "blue"

        self.is_flagged = False
        self.is_triggered = False
        self.is_covered = True
        self.adjacent = 0

    def get_triggered(self):
        return self.is_triggered

    def set_triggered(self):
        self.is_triggered = True

    def get_covered(self):
        return self.is_covered

    def uncover(self):
        self.is_covered=False

    def get_flagged(self):
        return self.is_flagged

    def set_flagged(self):
        self.is_flagged = not self.is_flagged

    def set_adjacent(self,adj):
        self.adjacent=adj
        pass

    def get_adjacent(self):
        return self.adjacent

    def get_colour(self):
        return self.colour

    def __str__(self):

        if self.get_flagged():
            return "F"

        if self.get_covered():
            return " "

        return str(self.get_adjacent())

    def __repr__(self):

        if self.get_flagged():
            return "F"

        if self.get_covered():
            return " "

        return str(self.get_adjacent())

def generate_board_colours(grid):
    board = [[colour_square() for x in range(grid)]for y in range(grid)]

    for y in range(grid):
        for x in range(grid):

            temp=0

            if(y > 0):
                if board[y-1][x].get_colour()==board[y][x].get_colour():
                    temp+=1

            if(x > 0):
                if board[y][x-1].get_colour()==board[y][x].get_colour():
                    temp+=1

            if(y < grid-1):
                if board[y+1][x].get_colour()==board[y][x].get_colour():
                    temp +=1

            if(x < grid-1):
                if board[y][x+1].get_colour()==board[y][x].get_colour():
                    temp +=1
            board[y][x].set_adjacent(temp)


    return board

def right_click_colours(grid,bombsrem,x,y):

    ret = 0

    if(grid[y][x]).get_covered():

        if grid[y][x].get_flagged():
            ret = 1
        elif bombsrem <= 0:
            return 0
        else:
            ret = -1

        grid[y][x].set_flagged()

    return ret

def left_click_colours(grid,x,y):

    grid_size = len(grid)

    c = grid[x][y].get_colour();

    if grid[y][x].get_covered():

        grid[y][x].uncover()

        if y > 0:
            if not grid[y - 1][x].get_covered():
                if grid[y][x].get_colour() == grid[y - 1][x].get_colour():
                    return False

        if x > 0:
            if not grid[y][x - 1].get_covered():
                if grid[y][x].get_colour() == grid[y][x - 1].get_colour():
                    return False

        if y < grid_size - 1:
            if not grid[y + 1][x].get_covered():
                if grid[y][x].get_colour() == grid[y + 1][x].get_colour():
                    return False

        if x < grid_size - 1:
            if not grid[y][x + 1].get_covered():
                if grid[y][x].get_colour() == grid[y][x + 1].get_colour():
                   return False
    return True

def detect_conflicting_spaces(grid):

    grid_size = len(grid)

    h=0

    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x].get_covered() == False:
                continue

            if y > 0:
                if grid[y][x].get_colour() == grid[y - 1][x].get_colour():
                    continue


            if x > 0:
                if grid[y][x].get_colour() == grid[y][x - 1].get_colour():
                    continue


            if y < grid_size - 1:
                if grid[y][x].get_colour() == grid[y + 1][x].get_colour():
                    continue


            if x < grid_size - 1:
                if grid[y][x].get_colour() == grid[y][x + 1].get_colour():
                    continue

            h+=1

    return h