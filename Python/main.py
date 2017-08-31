import tkinter as tk
import ms

bomb = 10
grid = 9

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Vanilla(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       buttonframe = tk.Frame(self)
       buttonframe.pack(side="top",fill="x",expand=False)

       bombs = tk.Entry(buttonframe, width=4)
       grids = tk.Entry(buttonframe, width=4)

       grids.insert(0, str(grid))
       bombs.insert(0, str(bomb))

       start = tk.Button(buttonframe,text="start",command=lambda: self.start_vanilla(int(grids.get()),int(bombs.get())))

       glabel = tk.Label(buttonframe,text="Grid Size: ")
       blabel = tk.Label(buttonframe,text="Mines: ")

       glabel.pack(side="left")
       grids.pack(side="left")
       blabel.pack(side="left")
       bombs.pack(side="left")
       start.pack(side="left")

       r = 0

   def start_vanilla(self,grid,bomb):
       self.game = ms.generate_board(grid,bomb)
       interface = tk.Frame(self)
       interface.pack(side="top",fill="x",expand=False)

       bombs_remaining=bomb

       brem = tk.Label(interface,text="Bombs Remaining: "+str(bombs_remaining))
       brem.pack(side="left",expand=False)

       gamewindow = tk.Frame(self)
       gamewindow.pack(side="top",fill="x",expand=False)

       for i in range(0,grid-1):
           for j in range(0,grid-1):
               tk.Button(gamewindow,width=3,text=str(self.game[i][j]),command=lambda: self.handle_left_click(self.game,gamewindow,j,i)).grid(row=i,column=j)

   def handle_left_click(self,window,j,i):
       ms.left_click(self.game,j,i)


class Hexagon(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       #label = tk.Label(self, text="This is Hexagon")
       #label.pack(side="top", fill="both", expand=True)

class Colours(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       #label = tk.Label(self, text="This is Colours")
       #label.pack(side="top", fill="both", expand=True)

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