from tkinter import *
import logging
from server.window import Window

win = Tk()
win.geometry("800x800")
app = Window(win)
win.mainloop()

