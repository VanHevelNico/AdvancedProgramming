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
        self.master.title("User GUI")
        self.pack( expand=1)

        Label(self, text="Naam").grid(row=0, sticky=W)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=1)
        
        Label(self, text="Nickname").grid(row=0,column=1, sticky=W)
        self.entry_nickname = Entry(self, width=40)
        self.entry_nickname.grid(row=1, column=1)
                
        Label(self, text="Email").grid(row=2, sticky=W)
        self.entry_email = Entry(self, width=40)
        self.entry_email.grid(row=3, columnspan= 2, sticky=E + W)

        self.buttonLogin = Button(self, text="Login",command=self.buttonInloggen)
        self.buttonLogin.grid(row=4, sticky=E + W)

        self.buttonRegister = Button(self, text="Registeren", command=self.buttonRegistreren)
        self.buttonRegister.grid(row=4,column=1, sticky=E + W)

        self.errorLabel = Label(self, text="")
        self.errorLabel.grid(row=8)

        self.buttonClose = Button(self, text="Sluiten", command=self.buttonSluiten)
        self.buttonClose.grid(row=8,column=1, sticky=E + W)

        Grid.rowconfigure(self, 12, weight=2)
        Grid.columnconfigure(self, 10, weight=1)

    # def __del__(self):
    #     print("CloseConnection aanroepen")
    #     self.close_connection()  

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

    def buttonSluiten(self):
        print("CloseConnection aanroepen")
        self.close_connection()
        # root.destroy()

    def buttonInloggen(self):
        global login
        try:
            print("inloggen")

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
            print(f"doorgestuurde berivht: {str(entry)}")
                    
            # resultaat afwachten
            print(f"Wachten op antwoord")
            code = pickle.load(self.in_out_server)
            print(code)
            if code == "OK":
                print("Ingelogd")
                login = entry

                Label(self, text="Begin date: format yyyy-mm-dd").grid(row=9, column=0)
                Label(self, text="End date: format yyyy-mm-dd", pady=10).grid(row=9, column=1)

                self.entry_begin = Entry(self)
                self.entry_begin.grid(row=10, column=0)
                self.entry_end = Entry(self)
                self.entry_end.grid(row=10, column=1)

                self.buttonOrderByDate = Button(self, text="Get launches between given dates", command=self.orderedByDate)
                self.buttonOrderByDate.grid(row=11, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                self.buttonGetByCustomer = Button(self, text="Get launches by customer", command=self.orderedByCustomer)
                self.buttonGetByCustomer.grid(row=12, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                self.buttonGetByCustomer = Button(self, text="Show launch year grah", command=self.graphLaunchYear)
                self.buttonGetByCustomer.grid(row=13, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                self.buttonGetByCustomer = Button(self, text="Show customers grah", command=self.graphCustomer)
                self.buttonGetByCustomer.grid(row=14, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

                Label(self, text="Output:").grid(row=15)
                self.scrollbar = Scrollbar(self, orient=VERTICAL)
                self.lstOutput = Listbox(self, yscrollcommand=self.scrollbar.set)
                self.scrollbar.config(command=self.lstOutput.yview)

                self.lstOutput.grid(row=16, column=0, columnspan=2,  sticky=N + S + E + W)
                self.scrollbar.grid(row=16, column=0, sticky=N + S) 

                # os.system(f'python {dashboard_script}')
            elif code == "NOK":
                self.errorLabel['text'] = "Er is geen account gevonden met deze inloggegevens"
            
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Inloggen", "Something has gone wrong...")

    def buttonRegistreren(self):
        try:
            print("registreren")

            # Errorbox leegmaken
            self.errorLabel['text'] = ""

            # Ingegeven waarden opslaan
            naam = str(self.entry_name.get())
            nickname = str(self.entry_nickname.get())
            email = str(self.entry_email.get())

            # regex van een email
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

            # Checken of ingegeven woorden voldoen aan de eisen
            if any(not c.isalpha() for c in naam):
                self.errorLabel['text'] = "De ingegeven naam bevat speciale tekens"
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

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Registreren", "Something has gone wrong...")

    def graphLaunchYear(self):
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

        root.mainloop()

    def graphCustomer(self):
        pickle.dump("GET_GRAPH", self.in_out_server)
        self.in_out_server.flush()
        result = pickle.load(self.in_out_server)
        dataframe = pd.DataFrame.from_dict(result, orient='index')
        root = Tk()
        df1 = dataframe
        df1 = df1.transpose()
        figure = Figure(figsize=(15,6))
        ax = figure.subplots()
        plot = sns.catplot(y="Customer Name",data=df1, kind="count", ax=ax)
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        root.mainloop()

    def fillCombobox(self):
        try:
            pickle.dump("FILL_COMBOBOX", self.in_out_server)
            self.in_out_server.flush()
            
            # resultaat afwachten
            result = pickle.load(self.in_out_server)
            result = result.tolist()
            self.comboCustomers = Combobox(self,values=result)
            self.comboCustomers.grid(row=4, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")

    def orderedByCustomer(self):
        try:
            self.lstOutput.delete(0, END)
            customer = self.comboCustomers.get()
            pickle.dump("GET_BY_CUSTOMER", self.in_out_server)  
            entry = customer
            pickle.dump(entry, self.in_out_server)
            self.in_out_server.flush()
            
            # resultaat afwachten
            result = pickle.load(self.in_out_server)
            print(result)
            result = result.to_dict()
            print(result)
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

    def orderedByDate(self):
        try:
            self.lstOutput.delete(0, END)
            pickle.dump("GET_BY_DATE", self.in_out_server)

            start_date = str(self.entry_begin.get())
            end_date = str(self.entry_end.get())
    
            entry = {"start_date":start_date, "end_date":end_date}
            pickle.dump(entry, self.in_out_server)
            self.in_out_server.flush()
            
            # resultaat afwachten
            result = pickle.load(self.in_out_server)
            result = result.to_dict()
            print(result)
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
        print("close connection funct started")
        global login
        try:
            pickle.dump("CLOSE", self.in_out_server)
            if len(login)==0:
                pickle.dump("NOLOGIN", self.in_out_server)
                print("Nologin")
                self.in_out_server.flush()
                logging.info("Close connection with server...")
                print("close")
                self.socket_to_server.close()
            else:
                pickle.dump(login, self.in_out_server)
                self.in_out_server.flush()
                print("waiting for response")
                logging.info("Close connection with server...")
                self.socket_to_server.close()     
        except:
            logging.error("Foutmelding:close connection with server failed")


logging.basicConfig(level=logging.INFO)

root = Tk()
# root.geometry("400x300")
app = HomeScreenWindow(root)
root.mainloop()

