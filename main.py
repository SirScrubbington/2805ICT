import tkinter as tk
import ms
import cs
import time
import sqlite3
from sqlite3 import Error
import pytz
import calendar
import datetime

conn = None
bomb = 10
grid = 9

def to_datetime_from_utc(time_tuple):
    return datetime.fromtimestamp(calendar.timegm(time_tuple), tz=pytz.utc)

def create_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

def create_table(conn,sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def get_scores(conn,gamemode,grids,mines):
    sql=""
    if gamemode == "Colours":
        sql = "SELECT * FROM SCORES WHERE GAMEMODE = '" + str(gamemode) + "' AND GRIDSIZE = " + str(grids)+" ORDER BY _TIME ASC;"
        print(sql)
    else:
        sql = "SELECT * FROM SCORES WHERE GAMEMODE = '" + str(gamemode) + "' AND GRIDSIZE = "+str(grids)+" AND BOMBS = "+str(mines)+" ORDER BY _TIME ASC;"
        print(sql)

    try:
        c = conn.cursor()
        c.execute(sql)
        rows=c.fetchall()
        r = []
        for row in rows:
            r.append(row)
        return r
    except Error as e:
        print(e)

# insert_score("PLAYER", "Colours", self.bombref, self.grid, time)

def insert_score(conn,name,gamemode,bombc,gridsiz,time):
    try:
        c = conn.cursor()
        sql = "INSERT INTO SCORES (USERNAME, GAMEMODE,BOMBS,GRIDSIZE,_TIME) VALUES ('"+str(name)+"','"+str(gamemode)+"',"+str(bombc)+","+str(gridsiz)+","+str(time)+");"
        print(sql)
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

def insert_row(conn,table,data):
     try:
         c = conn.cursor()

         sql = "INSERT INTO "+table+" VALUES ("

         for i in range(0,len(data)):
             if(i > 0):
                sql += ","
             if(isinstance(data[i],str)):
                 temp = data[i].replace("'","’")
                 sql +="'"+temp+"'"
             else:
                 sql +=str(data[i])
         sql+=");"
         print(sql)
         c.execute(sql)
         conn.commit()
     except Error as e:
         print(sql)
         print(e)

def popup_window(wl,time):
    toplevel = tk.Toplevel()
    toplevel.focus_force()
    # Lost the Game
    if wl == False:
        label1=tk.Label(toplevel,text="You Lose! Time Taken: "+str(time) + " seconds.",height=0,width=50)
        label1.pack()
    # Won the Game
    else:
        label1 = tk.Label(toplevel, text="You Win! Time Taken: " + str(time) + " seconds.", height=0, width=50)
        label1.pack()


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Vanilla(Page):

   def decide_sprite(self,y,x):
       dir = "img/gif/"
       # possible bomb
       if self.game[y][x].get_flagged():
           img = tk.PhotoImage(file=dir + "flagged.gif")
           return img

       # completely blank
       if self.game[y][x].get_covered():
           img = tk.PhotoImage(file=dir+"unchecked.gif")
           return img

       # is triggered bomb
       if self.game[y][x].get_triggered():
           img = tk.PhotoImage(file=dir+"bomb-triggered.gif")
           return img

       # is bomb
       if self.game[y][x].get_bomb():
           img = tk.PhotoImage(file=dir+"bomb-revealed.gif")
           return img

       # has adjacent bomb
       if self.game[y][x].get_adjacent() > 0:
           img = tk.PhotoImage(file=dir+str(self.game[y][x].get_adjacent())+"-adj.gif")
           return img

       # is blank
       if self.game[y][x].get_adjacent() == 0:
           img = tk.PhotoImage(file=dir+"blank.gif")
           return img

   def __init__(self, *args, **kwargs):

       self.timer = 0

       Page.__init__(self, *args, **kwargs)
       buttonframe = tk.Frame(self)
       buttonframe.pack(side="top",fill="x",expand=False)

       bombs = tk.Entry(buttonframe, width=4)
       grids = tk.Entry(buttonframe, width=4)

       grids.insert(0, str(grid))
       bombs.insert(0, str(bomb))

       start = tk.Button(buttonframe,text="start",command=lambda: self.start(int(grids.get()),int(bombs.get())))

       glabel = tk.Label(buttonframe,text="Grid Size: ")
       blabel = tk.Label(buttonframe,text="Mines: ")

       glabel.pack(side="left")
       grids.pack(side="left")
       blabel.pack(side="left")
       bombs.pack(side="left")
       start.pack(side="left")

       self.game = None

       r = 0

   def start_timer(self):
       self.timer = time.time()
       pass

   def get_time(self):
       finaltime = time.time() - self.timer
       return finaltime

   def start(self,grid,bomb):

       if self.game != None:
           self.gamewindow.pack_forget()
           self.gamewindow.destroy()

       self.game = ms.generate_board(grid,bomb)
       interface = tk.Frame(self)
       interface.pack(side="top",fill="x",expand=False)

       self.bombc = bomb
       self.gridsiz = grid

       self.bombsrem = bomb
       self.load_game_board()
       self.start_timer()

   def load_game_board(self):
       self.gamewindow = tk.Frame(self)
       w = tk.Canvas(self.gamewindow,width=640,height=640)
       self.sprite_grid = {}

       # UI Elements
       self.bombref = []
       i=0
       for n in str(self.bombsrem):
           bombs = tk.PhotoImage(file="img/gif/" + n + ".gif")
           bomblabel = tk.Label(self.gamewindow, image=bombs)
           bomblabel.image = bombs
           self.bombref.append(bomblabel)
           w.create_image(i*16+10,0+20,image=bombs)
           i+=1

       # Game Board
       for i in range(0,len(self.game)):
           for j in range(0,len(self.game)):
               temp = self.decide_sprite(i,j)
               templabel = tk.Label(self.gamewindow,image=temp)
               templabel.image= temp
               self.sprite_grid[(i,j)]=templabel
               w.create_image((i*16)+10,(j*16)+10+32,image=temp,tags="("+str(i)+","+str(j)+")")
               w.tag_bind("("+str(i)+","+str(j)+")",'<ButtonPress-1>',lambda gw = self.gamewindow,s_j=j,s_i=i: self.handle_left_click(gw,s_j,s_i))
               w.tag_bind("("+str(i)+","+str(j)+")",'<ButtonPress-3>',lambda gw = self.gamewindow,s_j=j,s_i=i: self.handle_right_click(gw,s_j,s_i))
               pass
       w.pack()
       self.gamewindow.pack(side="left",fill="x",expand=True)

   def reload_game_board(self):
       self.gamewindow.pack_forget()
       self.gamewindow.destroy()
       self.load_game_board()
       if self.bombsrem == 0:
           print("Checking solution...")
           sol = ms.check_solution(self.game)
           if sol:
               print("Solution reached!")
               gwlabel=tk.Label(self.gamewindow,text="You Win!")
               gwlabel.pack(side="left",fill="x",expand=True)
               time = self.get_time()
               popup_window(True, time)
               insert_score(conn, "PLAYER", "Vanilla", self.bombc,self.gridsiz, time)

   def handle_left_click(self,window,j,i):
       print('Calling for',j,i)
       bomb = ms.left_click(self.game,j,i)

       if bomb == -1:
            self.gameover(j,i)
       self.reload_game_board()

   def handle_right_click(self,window,j,i):
       self.bombsrem += ms.right_click(self.game,self.bombsrem,j,i)
       self.reload_game_board()


   def gameover(self,j,i):
       self.game[i][j].set_triggered()
       for y in self.game:
           for x in y:
               if x.get_flagged():
                   x.set_flagged()
               x.uncover()

       time = self.get_time()
       popup_window(False,time)
       print(time)

class Hexagon(Page):

   def start_timer(self):
       self.timer = time.time()
       pass

   def get_time(self):
       finaltime = time.time() - self.timer
       return finaltime

   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

   def decide_sprite(self, y, x):
       dir = "img/gif/"
       # possible bomb
       if self.game[y][x].get_flagged():
           img = tk.PhotoImage(file=dir + "flagged-hex.gif")
           return img

       # completely blank
       if self.game[y][x].get_covered():
           img = tk.PhotoImage(file=dir + "unchecked-hex.gif")
           return img

       # is triggered bomb
       if self.game[y][x].get_triggered():
           img = tk.PhotoImage(file=dir + "bombtriggered-hex.gif")
           return img

       # is bomb
       if self.game[y][x].get_bomb():
           img = tk.PhotoImage(file=dir + "bombreveal-hex.gif")
           return img

       # has adjacent bomb
       if self.game[y][x].get_adjacent() > 0:
           img = tk.PhotoImage(file=dir + str(self.game[y][x].get_adjacent()) + "-hex.gif")
           return img

       # is blank
       if self.game[y][x].get_adjacent() == 0:
           img = tk.PhotoImage(file=dir + "blank-hex.gif")
           return img

   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       buttonframe = tk.Frame(self)
       buttonframe.pack(side="top", fill="x", expand=False)

       bombs = tk.Entry(buttonframe, width=4)
       grids = tk.Entry(buttonframe, width=4)

       grids.insert(0, str(grid))
       bombs.insert(0, str(bomb))

       start = tk.Button(buttonframe, text="start", command=lambda: self.start(int(grids.get()), int(bombs.get())))

       glabel = tk.Label(buttonframe, text="Grid Size: ")
       blabel = tk.Label(buttonframe, text="Mines: ")

       glabel.pack(side="left")
       grids.pack(side="left")
       blabel.pack(side="left")
       bombs.pack(side="left")
       start.pack(side="left")

       self.game = None

       r = 0

   def start(self, grid, bomb):

       if self.game != None:
           self.gamewindow.pack_forget()
           self.gamewindow.destroy()

       self.game = ms.generate_board_hex(grid, bomb)
       interface = tk.Frame(self)
       interface.pack(side="top", fill="x", expand=False)

       self.bombsrem = bomb

       self.bombc = bomb
       self.gridsiz = grid

       self.load_game_board()

       self.start_timer()

   def load_game_board(self):
       self.gamewindow = tk.Frame(self)
       w = tk.Canvas(self.gamewindow, width=640, height=640)
       self.sprite_grid = {}

       # UI Elements
       self.bombref = []
       i = 0
       for n in str(self.bombsrem):
           bombs = tk.PhotoImage(file="img/gif/" + n + ".gif")
           bomblabel = tk.Label(self.gamewindow, image=bombs)
           bomblabel.image = bombs
           self.bombref.append(bomblabel)
           w.create_image(i * 16 + 10, 0 + 20, image=bombs)
           i += 1

       r = 0

       # Game Board
       for i in range(0, len(self.game)):
           r = 0
           for j in range(0, len(self.game)):

               temp = self.decide_sprite(i, j)

               templabel = tk.Label(self.gamewindow, image=temp)

               templabel.image = temp

               self.sprite_grid[(i, j)] = templabel

               w.create_image((i * 16) + 10+(r*8), (j * 12)+ 10 + 32, image=temp, tags="(" + str(i) + "," + str(j) + ")")

               w.tag_bind("(" + str(i) + "," + str(j) + ")", '<ButtonPress-1>',
                          lambda gw=self.gamewindow, s_j=j, s_i=i: self.handle_left_click(gw, s_j, s_i))

               w.tag_bind("(" + str(i) + "," + str(j) + ")", '<ButtonPress-3>',
                          lambda gw=self.gamewindow, s_j=j, s_i=i: self.handle_right_click(gw, s_j, s_i))

               if (r == 0):
                   r = 1
               else:
                   r = 0
       w.pack()
       self.gamewindow.pack(side="left", fill="x", expand=True)

   def reload_game_board(self):
       self.gamewindow.pack_forget()
       self.gamewindow.destroy()
       self.load_game_board()
       if self.bombsrem == 0:
           print("Checking solution...")
           sol = ms.check_solution(self.game)
           if sol:
               print("Solution reached!")
               gwlabel = tk.Label(self.gamewindow, text="You Win!")
               gwlabel.pack(side="left", fill="x", expand=True)
               time = self.get_time()
               popup_window(True, time)
               insert_score(conn, "PLAYER", "Hexagon", self.bombc,self.gridsiz, time)

   def handle_left_click(self, window, j, i):
       print('Calling for', j, i)
       bomb = ms.left_click_hex(self.game, j, i)

       if bomb == -1:
           self.gameover(j, i)
       self.reload_game_board()

   def handle_right_click(self, window, j, i):
       self.bombsrem += ms.right_click(self.game, self.bombsrem, j, i)
       self.reload_game_board()

   def gameover(self, j, i):
       self.game[i][j].set_triggered()
       for y in self.game:
           for x in y:
               if x.get_flagged():
                   x.set_flagged()
               x.uncover()
       time = self.get_time()
       popup_window(False, time)
       print(time)

class Colours(Page):

   def start_timer(self):
       self.timer = time.time()
       pass

   def get_time(self):
       finaltime = time.time() - self.timer
       return finaltime

   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

   def decide_sprite(self, y, x):
       dir = "img/gif/"
       # possible bomb
       if self.game[y][x].get_flagged():
           img = tk.PhotoImage(file=dir + "flagged.gif")
           return img

       # completely blank
       if self.game[y][x].get_covered():
           img = tk.PhotoImage(file=dir + "unchecked.gif")
           return img

       # has adjacent bomb
       if self.game[y][x].get_adjacent() > 0:
           img = tk.PhotoImage(file=dir + str(self.game[y][x].get_colour()) + "-" + str(self.game[y][x].get_adjacent()) + ".gif")
           return img

       # is blank
       if self.game[y][x].get_adjacent() == 0:
           img = tk.PhotoImage(file=dir + str(self.game[x][y].get_colour()) + ".gif")
           return img

   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       buttonframe = tk.Frame(self)
       buttonframe.pack(side="top", fill="x", expand=False)

       grids = tk.Entry(buttonframe, width=4)

       grids.insert(0, str(grid))

       start = tk.Button(buttonframe, text="start", command=lambda: self.start(int(grids.get())))

       glabel = tk.Label(buttonframe, text="Grid Size: ")

       glabel.pack(side="left")
       grids.pack(side="left")
       start.pack(side="left")

       self.game = None

       r = 0

   def start(self, grid):

       if self.game != None:
           self.gamewindow.pack_forget()
           self.gamewindow.destroy()

       self.game = cs.generate_board_colours(grid)
       interface = tk.Frame(self)
       interface.pack(side="top", fill="x", expand=False)

       self.bombsrem = bomb

       self.gridsiz = grid

       self.load_game_board()

       self.start_timer()

   def load_game_board(self):
       self.gamewindow = tk.Frame(self)
       w = tk.Canvas(self.gamewindow, width=640, height=640)
       self.sprite_grid = {}

       # UI Elements
       self.bombref = []
       i = 0
       for n in str(self.bombsrem):
           bombs = tk.PhotoImage(file="img/gif/" + n + ".gif")
           bomblabel = tk.Label(self.gamewindow, image=bombs)
           bomblabel.image = bombs
           self.bombref.append(bomblabel)
           w.create_image(i * 16 + 10, 0 + 20, image=bombs)
           i += 1

       # Game Board
       for i in range(0, len(self.game)):
           for j in range(0, len(self.game)):
               temp = self.decide_sprite(i, j)
               templabel = tk.Label(self.gamewindow, image=temp)
               templabel.image = temp
               self.sprite_grid[(i, j)] = templabel
               w.create_image((i * 16) + 10, (j * 16) + 10 + 32, image=temp, tags="(" + str(i) + "," + str(j) + ")")
               w.tag_bind("(" + str(i) + "," + str(j) + ")", '<ButtonPress-1>',
                          lambda gw=self.gamewindow, s_j=j, s_i=i: self.handle_left_click(gw, s_j, s_i))
               w.tag_bind("(" + str(i) + "," + str(j) + ")", '<ButtonPress-3>',
                          lambda gw=self.gamewindow, s_j=j, s_i=i: self.handle_right_click(gw, s_j, s_i))
               pass
       w.pack()
       self.gamewindow.pack(side="left", fill="x", expand=True)

   def reload_game_board(self):
       self.gamewindow.pack_forget()
       self.gamewindow.destroy()
       self.load_game_board()
       if self.bombsrem == 0:
           print("Checking solution...")
           sol = cs.detect_conflicting_spaces(self.game)
           if sol == 0:
               print("Solution reached!")
               gwlabel = tk.Label(self.gamewindow, text="You Win!")
               gwlabel.pack(side="left", fill="x", expand=True)
               time = self.get_time()
               popup_window(True, time)
               insert_score(conn,"PLAYER", "Colours",0,self.gridsiz, time)

   def handle_left_click(self, window, j, i):
       print('Calling for', j, i)
       state = cs.left_click_colours(self.game, j, i)

       if state == False:
           self.gameover(j,i)

       self.reload_game_board()

   def handle_right_click(self, window, j, i):
       self.bombsrem += cs.right_click_colours(self.game, self.bombsrem, j, i)
       self.reload_game_board()

   def gameover(self, j, i):
       self.game[i][j].set_triggered()
       for y in self.game:
           for x in y:
               if x.get_flagged():
                   x.set_flagged()
               x.uncover()
       time = self.get_time()
       popup_window(False, time)
       print(time)

class HighScores(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        buttonframe = tk.Frame(self)
        buttonframe.pack(side="top",fill="x",expand=False)

        gamemode=tk.Entry(buttonframe,width=8)
        bombs=tk.Entry(buttonframe,width=4)
        grids=tk.Entry(buttonframe,width=4)

        gamemode.insert(0,"Vanilla")
        bombs.insert(0,str(8))
        grids.insert(0,str(9))

        glabel = tk.Label(buttonframe, text="Grid Size: ")
        blabel = tk.Label(buttonframe, text="Mines: ")
        gmlabel = tk.Label(buttonframe,text="Game Mode: ")

        search = tk.Button(buttonframe,text="Search",command=lambda: self.search(gamemode.get(),grids.get(),bombs.get()))

        gmlabel.pack(side="left")
        gamemode.pack(side="left")
        glabel.pack(side="left")
        grids.pack(side="left")
        blabel.pack(side="left")
        bombs.pack(side="left")
        search.pack(side="left")

        self.scorepanel = tk.Frame(self)
        self.scorepanel.pack(side="top",fill="x",expand=False)

    def search(self,gamemode,grids,bombs):
        self.scorepanel.pack_forget()
        self.scorepanel = tk.Frame(self)
        self.scorepanel.pack(side="top", fill="x", expand=False)
        s = get_scores(conn,gamemode,grids,bombs)
        labels = []
        l = tk.Label(self.scorepanel,text="| Ranking | Name | Gamemode | Bombs | Grid Size | Score |",justify="left",anchor="w")
        l.pack(side="top")
        labels.append(l)
        j=0
        for i in s:
            print(i)
            j+=1
            if(j>10):
                break
            l = tk.Label(self.scorepanel,text="| "+str(j)+". | "+str(i[0])+" | "+str(i[1])+" | "+str(i[2])+" | "+str(i[3])+" | "+str(i[4]),justify="left",anchor="w")
            l.pack(side="top")
            labels.append(l)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Vanilla(self)
        p2 = Hexagon(self)
        p3 = Colours(self)
        p4 = HighScores(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container,x=0,y=0,relwidth=1,relheight=1)

        b1 = tk.Button(buttonframe, text="Standard", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Hexagon", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Colours", command=p3.lift)
        b4 = tk.Button(buttonframe, text="High Scores",command=p4.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")

        p1.show()

if __name__ == "__main__":
    conn = create_db("scores.db")
    create_table(conn,"CREATE TABLE SCORES("
                      "USERNAME VARCHAR(16),"
                      "GAMEMODE VARCHAR(16),"
                      "BOMBS INTEGER,"
                      "GRIDSIZE INTEGER,"
                      "_TIME DOUBLE"
                      ")")

    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both",expand=True)
    main.master.title("Minesweeper")
    main.master.iconbitmap("img/ico/icon.ico")
    root.wm_geometry("400x400")
    root.mainloop()