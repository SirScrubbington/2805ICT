import tkinter as tk
import ms
import time

bomb = 10
grid = 9

class StopWatch(tk.Frame):
    def __init__(self,parent=None,**kw):
        tk.Frame.__init__(self,parent,kw)
        self._start = 0.0
        self._elapsedtime=0.0
        self._running=0
        self.timestr=""
        self.makeWidgets()

    def makeWidgets(self):
        l = tk.Label(self,textvariable=self.timestr)
        self.setTime(self._elapsedtime)
        l.pack(fill="x",expand=False,pady=2,padx=2)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

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

   def start(self,grid,bomb):

       if self.game != None:
           self.gamewindow.pack_forget()
           self.gamewindow.destroy()

       self.game = ms.generate_board(grid,bomb)
       interface = tk.Frame(self)
       interface.pack(side="top",fill="x",expand=False)

       self.bombsrem = bomb

       self.load_game_board()

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

class Hexagon(Page):
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

       self.load_game_board()

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

class Colours(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Vanilla(self)
        p2 = Hexagon(self)
        p3 = Colours(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Standard", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Hexagon", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Colours", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()