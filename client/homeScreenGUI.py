from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
import pickle

from data.Registreren import Registreren

class HomeScreenWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()
        self.makeConnnectionWithServer()

    def init_window(self):
        self.master.title("Inloggen")
        self.pack( expand=1)

        Label(self, text="Naam").grid(row=0)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=1)
        
        Label(self, text="Nickname").grid(row=2)
        self.entry_nickname = Entry(self, width=40)
        self.entry_nickname.grid(row=3)
                
        Label(self, text="Email").grid(row=4)
        self.entry_email = Entry(self, width=40)
        self.entry_email.grid(row=5)

        self.buttonLogin = Button(self, text="Login", command=lambda: self.buttonInloggen(root))
        self.buttonLogin.grid(row=6, pady=(20, 10), padx=(5, 5), sticky=N + S + E + W)

        self.buttonRegister = Button(self, text="Registeren", command=self.buttonRegistreren)
        self.buttonRegister.grid(row=7, pady=(0, 10), padx=(5, 5), sticky=N + S + E + W)

        self.errorLabel = Label(self, text="")
        self.errorLabel.grid(row=8)


        Grid.rowconfigure(self, 8, weight=2)
        Grid.columnconfigure(self, 1, weight=1)

    def __del__(self):
        self.close_connection()

    def makeConnnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            # NIEUW
            self.in_out_server = self.socket_to_server.makefile(mode='rwb')
            logging.info("Open connection with server succesfully")
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Stopafstand - foutmelding", "Something has gone wrong...")

    def buttonInloggen(self):
        print("inloggen")

    def buttonRegistreren(self):
        try:
            print("registreren")
            pickle.dump("REGISTREREN", self.in_out_server)

            naam = str(self.entry_name.get())
            nickname = str(self.entry_nickname.get())
            email = str(self.entry_email.get())
    
            entry = {"name":naam, "nickname":nickname, "email":email, "isonline": 0}
            pickle.dump(entry, self.in_out_server)
            self.in_out_server.flush()
            
            # # resultaat afwachten
            # r1 = pickle.load(self.in_out_server)
            # self.label_resultaat['text'] = "{0}".format(s1.som)

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("CLOSE", self.in_out_server)
            self.in_out_server.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding:close connection with server failed")


logging.basicConfig(level=logging.INFO)

root = Tk()
# root.geometry("400x300")
app = HomeScreenWindow(root)
root.mainloop()

