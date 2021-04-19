from tkinter import *
import logging

import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

from client.homeScreenGUI import HomeScreenWindow

# win = Tk()
# win.geometry("800x800")
# app = HomeScreenWindow(win)
# win.mainloop()

win = Tk()
# root.geometry("400x300")
app = HomeScreenWindow(win)
win.mainloop()
