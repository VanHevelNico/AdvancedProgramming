import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
from tkinter import *
import pickle


class RegisteredWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Registered users")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Registered users:").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstRegistered = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstRegistered.yview)

        self.lstRegistered.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        
        reader = open("./data/Gebruikers.txt",mode="rb")
        self.lstRegistered.delete(0,END)
        users = pickle.load(reader)
        for user in users:
            userString = "Name: " + user['name'] + "   Nickname: " + user['nickname'] + "   Email: " + user['email']
            self.lstRegistered.insert(END,userString)
            self.lstRegistered.insert(END,"                                          --------------------------------------------------                                          ")

