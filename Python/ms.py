import random as rand

class square:
    def __init__(self):
        self.is_bomb=False
        self.is_flagged=False
        self.is_covered=True
        self.adjacent=0

    def get_covered(self):
        return self.is_covered

    def uncover(self):
        self.is_covered=False

    def get_bomb(self):
        return self.is_bomb

    def set_bomb(self):
        self.is_bomb = True

    def get_flagged(self):
        return self.is_flagged

    def set_flagged(self):
        self.is_flagged = not self.is_flagged

    def set_adjacent(self,adj):
        self.adjacent=adj
        pass

    def get_adjacent(self):
        return self.adjacent

    def __str__(self):

        if self.get_covered():
            return " "

        if self.get_bomb():
            return "B"
        return str(self.get_adjacent())

    def __repr__(self):

        if self.get_covered():
            return " "

        if self.get_bomb():
            return "B"
        return str(self.get_adjacent())

def flag(grid,x,y):
    if(grid[y][x]).get_covered():
        grid[y][x].set_flagged()

def left_click(grid,x,y):

    grid_size = len(grid)

    if grid[y][x].get_covered():
        if grid[y][x].get_bomb():
            return -1
        if grid[y][x].get_adjacent() > 0:
            grid[y][x].uncover()
            # implement game winning code here

        if grid[y][x].get_adjacent() == 0:
            grid[y][x].uncover()

            if (y > 0):
                if(not grid[y-1][x].get_flagged()):
                    left_click(grid,x,y-1);

            if (x > 0):
                if (not grid[y][x-1].get_flagged()):
                    left_click(grid,x-1,y);

            if (y < grid_size - 1):
                if not grid[y+1][x].get_flagged():
                    left_click(grid,x,y+1)

            if (x < grid_size - 1):
                if not grid[y][x+1].get_flagged():
                    left_click(grid,x+1,y)

            if (y > 0 and x > 0):
                if not grid[y-1][x-1].get_flagged():
                    left_click(grid,x-1,y-1)

            if (y < grid_size - 1 and x < grid_size - 1):
                if not grid[y+1][x+1].get_flagged():
                    left_click(grid,x+1,y+1)

            if (y < grid_size - 1 and x > 0):
                if not grid[y+1][x-1].get_flagged():
                    left_click(grid,x-1,y+1)

            if (y > 0 and x < grid_size - 1):
                if not grid[y-1][x+1].get_flagged():
                    left_click(grid,x+1,y-1)

def generate_board(grid,bomb):
    board = [[square() for x in range(grid)]for y in range(grid)]

    i=0
    while(i<bomb):
        tx = rand.randrange(0,grid-1)
        ty = rand.randrange(0,grid-1)

        if board[ty][tx].get_bomb() == False:
            board[ty][tx].set_bomb()
            i+=1

    for y in range(grid):

        for x in range(grid):
            if board[y][x].get_bomb() == True:
                continue

            temp=0

            if(y > 0):
                if board[y-1][x].get_bomb()==True:
                    temp+=1

            if(x > 0):
                if board[y][x-1].get_bomb()==True:
                    temp+=1

            if(y < grid-1):
                if board[y+1][x].get_bomb()==True:
                    temp +=1

            if(x < grid-1):
                if board[y][x+1].get_bomb()==True:
                    temp +=1

            if(y > 0 and x > 0):
                if board[y-1][x-1].get_bomb()==True:
                    temp +=1

            if(y < grid-1 and x < grid-1):
                if board[y+1][x+1].get_bomb()==True:
                    temp +=1

            if(y < grid -1 and x > 0):
                if board[y+1][x-1].get_bomb()==True:
                    temp +=1

            if(y > 0 and x < grid -1):
                if board[y-1][x+1].get_bomb()==True:
                    temp +=1

            board[y][x].set_adjacent(temp)


    return board

def print_board(grid):
    print(grid)