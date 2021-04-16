from tkinter import *
import logging
from client.homeScreenGUI import HomeScreenWindow

win = Tk()
win.geometry("800x800")
app = HomeScreenWindow(win)
win.mainloop()
