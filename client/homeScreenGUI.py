import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

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
import re
import os
sys.path[0] = str(Path(sys.path[0]).parent)
folder = os.path.dirname(os.path.abspath(__file__))
dashboard_script = os.path.join(folder,'gui_dashboard.py')

login = {}
class HomeScreenWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()
        self.makeConnnectionWithServer()

    def init_window(self):
        logging.info("Starting user GUI")
        self.master.title("User GUI")
        self.pack( expand=1)

        self.buttonClose = Button(self, text="Sluiten", command=self.logout)
        self.buttonClose.grid(row=0,column=2, sticky=E + W)

        Label(self, text="Naam").grid(row=1, sticky=W)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=2)
        
        Label(self, text="Nickname").grid(row=1,column=1, sticky=W)
        self.entry_nickname = Entry(self, width=40)
        self.entry_nickname.grid(row=2, column=1)
                
        Label(self, text="Email").grid(row=3, sticky=W)
        self.entry_email = Entry(self, width=40)
        self.entry_email.grid(row=4, columnspan= 2, sticky=E + W)

        self.buttonLogin = Button(self, text="Login",command=self.login)
        self.buttonLogin.grid(row=5, sticky=E + W)

        self.buttonRegister = Button(self, text="Registeren", command=self.register)
        self.buttonRegister.grid(row=5,column=1, sticky=E + W)

        self.errorLabel = Label(self, text="")
        self.errorLabel.grid(row=8)

        Grid.rowconfigure(self, 12, weight=2)
        Grid.columnconfigure(self, 10, weight=1)

    # def __del__(self):
    #     print("CloseConnection aanroepen")
    #     self.close_connection()  

    def fillCombobox(self):
        try:
            logging.info("Getting data from server to fill combobox")
            pickle.dump("FILL_COMBOBOX", self.in_out_server)
            self.in_out_server.flush()
            
            # resultaat afwachten
            result = pickle.load(self.in_out_server)
            result = result.tolist()
            self.comboCustomers = Combobox(self,values=result)
            self.comboCustomers.grid(row=12, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")

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
            messagebox.showinfo("Fout!", "Something has gone wrong...")

    def logout(self):
        logging.info("CloseConnection aanroepen")
        self.close_connection()
        # root.destroy()

    def login(self):
        global login
        try:
            logging.info("Trying to log in")

            # Errorbox leegmaken
            self.errorLabel['text'] = ""

            # Server laten weten dat het om een login gaat
            pickle.dump("INLOGGEN", self.in_out_server)

            # Ingegeven waarden opslaan
            naam = str(self.entry_name.get())
            nickname = str(self.entry_nickname.get())
            email = str(self.entry_email.get())
            entry = {"name":naam, "nickname":nickname, "email":email, "isonline": 0}

            # Deze dictionary naar de server
            pickle.dump(entry, self.in_out_server)
            self.in_out_server.flush()
            logging.info("Sent login request to server and waiting for answer")
                    
            # resultaat afwachten
            code = pickle.load(self.in_out_server)
            if code == "OK":
                logging.info("Login accepted")
                login = entry


                Label(self, text="Value 1: format yyyy-mm-dd or decimal").grid(row=9, column=0)
                Label(self, text="Value 2: format yyyy-mm-dd or decimal", pady=10).grid(row=9, column=1)

                self.entry_begin = Entry(self)
                self.entry_begin.grid(row=10, column=0)
                self.entry_end = Entry(self)
                self.entry_end.grid(row=10, column=1)

                self.buttonBetween = Button(self, text="Get launches (with payload) between value 1 and value 2", command=self.launchesBetween)
                self.buttonBetween.grid(row=11, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                self.buttonGetByCustomer = Button(self, text="Get launches by customer", command=self.launchesByCustomer)
                self.buttonGetByCustomer.grid(row=13, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                self.buttonGetByCustomer = Button(self, text="Show launch year graph", command=self.graphLaunchYear)
                self.buttonGetByCustomer.grid(row=14, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                self.buttonGetByCustomer = Button(self, text="Show customers graph", command=self.graphCustomer)
                self.buttonGetByCustomer.grid(row=15, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                Label(self, text="Output:").grid(row=16, sticky= W)
                self.scrollbar = Scrollbar(self, orient=VERTICAL)
                #self.scrollbarHorizontal = Scrollbar(self, orient=HORIZONTAL)
                self.lstOutput = Listbox(self, yscrollcommand=self.scrollbar.set)
                self.scrollbar.config(command=self.lstOutput.yview)

                self.lstOutput.grid(row=17, column=0, columnspan=2,  sticky=N + S + E + W)
                self.scrollbar.grid(row=17, column=0, sticky=N + S) 
                
                self.fillCombobox()

            elif code == "NOK":
                logging.info("Login not accepted")
                self.errorLabel['text'] = "Er is geen account gevonden met deze inloggegevens"
                logging.error("Er is geen account gevonden met deze inloggegevens")

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Inloggen", "Something has gone wrong...")

    def register(self):
        try:
            logging.info("Trying to register")

            # Errorbox leegmaken
            self.errorLabel['text'] = ""

            # Ingegeven waarden opslaan
            naam = str(self.entry_name.get())
            nickname = str(self.entry_nickname.get())
            email = str(self.entry_email.get())

            # regex van een email
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

            # Checken of ingegeven naam voldoen aan de eisen
            if any(not c.isalpha() for c in naam):
                self.errorLabel['text'] = "De ingegeven naam bevat speciale tekens"
                logging.error("De ingegeven naam bevat niet speciale tekens")
            else:
                if (re.search(regex, email)):

                    # Server laten weten dat het om een registratie gaat
                    pickle.dump("REGISTREREN", self.in_out_server)

                    # Dictionary maken van de ingegeven waarden
                    entry = {"name":naam, "nickname":nickname, "email":email, "isonline": 0}

                    # Deze dictionary naar de server
                    pickle.dump(entry, self.in_out_server)
                    self.in_out_server.flush()
                    
                    # resultaat afwachten
                    code = pickle.load(self.in_out_server)
                    self.errorLabel['text'] = code
                else:
                    self.errorLabel['text'] = "Het ingegeven e-mailadres is ongeldig"
                    logging.error("Het ingegeven e-mailadres is ongeldig")

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Registreren", "Something has gone wrong...")

    def graphLaunchYear(self):
        logging.info("Getting launch year graph")
        pickle.dump("GET_GRAPH", self.in_out_server)
        self.in_out_server.flush()
        result = pickle.load(self.in_out_server)
        dataframe = pd.DataFrame.from_dict(result, orient='index')
        root = Tk()
        df1 = dataframe
        df1 = df1.transpose()
        figure = Figure(figsize=(6, 6))
        ax = figure.subplots()
        plot = sns.countplot(x='Launch Year', data=df1, ax=ax)
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        pickle.dump("YEAR", self.in_out_server)
        self.in_out_server.flush()

        root.mainloop()

    def graphCustomer(self):
        logging.info("Get customer graph")
        pickle.dump("GET_GRAPH", self.in_out_server)
        self.in_out_server.flush()
        result = pickle.load(self.in_out_server)
        dataframe = pd.DataFrame.from_dict(result, orient='index')
        root = Tk()
        df1 = dataframe
        df1 = df1.transpose()
        figure = Figure(figsize=(15,6))
        ax = figure.subplots()
        plot = sns.countplot(y="Customer Name",data=df1, ax=ax)
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        pickle.dump("CUSTOMER", self.in_out_server)
        self.in_out_server.flush()

        root.mainloop()


    def launchesByCustomer(self):
        try:
            logging.info("Getting launchers by customer")
            self.lstOutput.delete(0, END)
            customer = self.comboCustomers.get()
            pickle.dump("GET_BY_CUSTOMER", self.in_out_server)  
            entry = customer
            pickle.dump(entry, self.in_out_server)
            self.in_out_server.flush()
            
            # resultaat afwachten
            result = pickle.load(self.in_out_server)
            result = result.to_dict()
            teller = 0
            value = ""
            count = result['Flight Number']
            count = count.keys()
            count = list(count)
            count = len(count)
            count = count 
            for teller in range(count):
                teller2 = teller +1
                for line in result:
                    current_dict = result[line]
                    current_dict_values = current_dict.keys()
                    current_dict_values = list(current_dict_values)[teller]
                    value += str(line) + ": " +str(current_dict[current_dict_values]) + " \n"
                self.lstOutput.insert(END,value)
                self.lstOutput.insert(END," --- ")
                teller = teller +1
                value = ""
    

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def launchesBetween(self):
        try:
            logging.info("Getting launchers between dates")
            self.lstOutput.delete(0, END)
            pickle.dump("BETWEEN", self.in_out_server)
            self.in_out_server.flush()

            value1 = str(self.entry_begin.get())
            value2 = str(self.entry_end.get())
            both = value1+value2

            entry = {"value1":value1, "value2":value2}

            if any(not c.isnumeric() for c in both):
                pickle.dump("DATE", self.in_out_server)
            else:
                pickle.dump("CARGO", self.in_out_server)
            self.in_out_server.flush()
            pickle.dump(entry, self.in_out_server)
            self.in_out_server.flush()
            
            # resultaat afwachten
            result = pickle.load(self.in_out_server)
            result = result.to_dict()
            teller = 0
            value = ""
            count = result['Flight Number']
            count = count.keys()
            count = list(count)
            count = len(count)
            count = count 
            for teller in range(count):
                teller2 = teller +1
                value += "Flight " + str(teller2) + ": \n"
                for line in result:
                    current_dict = result[line]
                    current_dict_values = current_dict.keys()
                    current_dict_values = list(current_dict_values)[teller]
                    value += str(line) + ": " +str(current_dict[current_dict_values]) + " \n"
                self.lstOutput.insert(END,value)
                self.lstOutput.insert(END," --- ")
                teller = teller +1
                value = ""

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")

    def close_connection(self):
        logging.info("Closing connection")
        global login
        try:
            pickle.dump("CLOSE", self.in_out_server)
            if len(login)==0:
                pickle.dump("NOLOGIN", self.in_out_server)
                self.in_out_server.flush()
                logging.info("Close connection with server...")
                self.socket_to_server.close()
            else:
                pickle.dump(login, self.in_out_server)
                self.in_out_server.flush()
                logging.info("Close connection with server...")
                self.socket_to_server.close()     
        except:
            logging.error("Foutmelding: close connection with server failed")


logging.basicConfig(level=logging.INFO)

root = Tk()
# root.geometry("400x300")
app = HomeScreenWindow(root)
root.mainloop()

