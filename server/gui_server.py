import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
from queue import Queue
from threading import Thread
from tkinter import *

from server.server import SommenServer
from server.gui_registered_users import RegisteredWindow
import pickle


class ServerWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.server = None
        self.thread_listener_queue=None
        self.init_messages_queue()



    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Server")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstlogs = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstlogs.yview)

        self.lstlogs.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        Label(self, text="Connected users:").grid(row=2)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstconnected = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstconnected.yview)

        self.lstconnected.grid(row=3, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=3, column=1, sticky=N + S)

        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = Button(self, textvariable=self.btn_text, command=self.start_stop_server)
        self.buttonServer.grid(row=4, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

        self.btn_text2 = StringVar()
        self.btn_text2.set("Registered users")       
        self.buttonRegistered = Button(self, textvariable=self.btn_text2, command=self.open_registered_users)
        self.buttonRegistered.grid(row=5, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    def open_registered_users(self):
        root = Tk()
        root.geometry("400x400")
        gui_server = RegisteredWindow(root)

    def start_stop_server(self):
        if self.server is not None:
            self.__stop_server()
        else:
            self.__start_server()

    def __stop_server(self):
        self.lstconnected.delete(0,END)
        self.server.stop_server()
        self.server = None
        logging.info("Server stopped")
        self.btn_text.set("Start server")

    def __start_server(self):
        self.server = SommenServer(socket.gethostname(), 9999, self.messages_queue)
        self.server.init_server()
        self.server.start()  # in thread plaatsen!
        logging.info("Server started")
        self.btn_text.set("Stop server")

    def init_messages_queue(self):
        self.messages_queue = Queue()
        self.thread_listener_queue = Thread(target=self.print_messsages_from_queue, name="Queue_listener_thread", daemon=True)
        self.thread_listener_queue.start()

    def print_messsages_from_queue(self):
        message = self.messages_queue.get()
        while message != "CLOSE_SERVER":
            #Logs
            self.lstlogs.insert(END, message)
            self.messages_queue.task_done()
            message = self.messages_queue.get()
            #Online users
            reader = open("./data/Gebruikers.txt",mode="rb")
            self.lstconnected.delete(0,END)
            users = pickle.load(reader)
            for user in users:
                if(user['isonline']==1):
                    userString = "Name: " + user['name'] + "   Nickname: " + user['nickname'] + "   Email: " + user['email']
                    self.lstconnected.insert(END,userString)
                    self.lstconnected.insert(END,"                                          --------------------------------------------------                                          ")



