import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
import pickle
from tkinter import *

from tkinter import messagebox
from tkinter.ttk import Combobox

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Dashboard(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.makeConnnectionWithServer()
        self.fillCombobox()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Dashboard")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Begin date: format yyyy-mm-dd").grid(row=0, column=0)
        Label(self, text="End date: format yyyy-mm-dd", pady=10).grid(row=0, column=1)

        self.entry_begin = Entry(self)
        self.entry_begin.grid(row=1, column=0)
        self.entry_end = Entry(self)
        self.entry_end.grid(row=1, column=1)

        self.buttonOrderByDate = Button(self, text="Get data ordered by date", command=self.orderedByDate)
        self.buttonOrderByDate.grid(row=3, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        Label(self, text="Get launches by customer").grid(row=0, column=1)

        self.buttonGetByCustomer = Button(self, text="Get data by customer", command=self.orderedByCustomer)
        self.buttonGetByCustomer.grid(row=5, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        self.buttonGetByCustomer = Button(self, text="Show launch year grah", command=self.graphLaunchYear)
        self.buttonGetByCustomer.grid(row=6, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        self.buttonGetByCustomer = Button(self, text="Show customers grah", command=self.graphCustomer)
        self.buttonGetByCustomer.grid(row=7, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        Label(self, text="Output:").grid(row=8)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstOutput = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstOutput.yview)

        self.lstOutput.grid(row=9, column=0, columnspan=2,  sticky=N + S + E + W)
        self.scrollbar.grid(row=9, column=0, sticky=N + S)             

        Grid.rowconfigure(self, 10, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

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
        figure = Figure(figsize=(9,9))
        ax = figure.subplots()
        plot = sns.countplot(y='Customer Name', data=df1, ax=ax)
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
            entry = {"customer":customer}
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

logging.basicConfig(level=logging.INFO)

root = Tk()
root.geometry("700x700")
app = Dashboard(root)
root.mainloop()
