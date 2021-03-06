import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

import logging
import threading
from threading import Thread
from tkinter import *

from server.gui_server import ServerWindow


def callback():
    # even controleren overlopen van actieve threads wanneer window gesloten wordt
    logging.debug("Active threads:")
    for thread in threading.enumerate():
        logging.debug(f">Thread name is {thread.getName()}.")
    root.destroy()

root = Tk()
root.geometry("600x600")
gui_server = ServerWindow(root)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()

