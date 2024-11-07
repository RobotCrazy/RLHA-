from tkinter import *

class CellArray():
    def __init__(self, root):
        self.board = [[0, 0, 0, 0, 0,]
                 [0, 0, 0, 0, 0,],
                 [0, 0, 0, 0, 0,],
                 [0, 0, 0, 0, 0,],
                 [0, 0, 0, 0, 0,],
                 [0, 0, 0, 0, 0,],]

class CellCanvas(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.initBoard()

    def initBoard(self):
        self.display = Canvas(root, width=500, height=500, borderwidth=5, background='white')
        self.display.grid()
        for r in range(10):
            for c in range(10):
                

root = Tk()
board = CellCanvas(root)
root.mainloop()