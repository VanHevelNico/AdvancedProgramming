import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

import threading
import pickle

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('database/database.csv')
class ClientHandler(threading.Thread):
    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue):
        threading.Thread.__init__(self)
        # connectie with client
        self.socket_to_client = socketclient
        # message queue -> link to gui server
        self.messages_queue = messages_queue
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        ClientHandler.numbers_clienthandlers += 1

    def run(self):
        Gebruikers_path = "database/Gebruikers.txt"
        socket_to_client = self.socket_to_client.makefile(mode='rwb')

        self.print_bericht_gui_server("Waiting for numbers...")
        commando = pickle.load(socket_to_client)
        print(commando)

        while commando != "CLOSE":
            if commando == "SOM":
                s1 = pickle.load(socket_to_client)  # SOM-object
                s1.som = s1.getal1 + s1.getal2
                pickle.dump(s1, socket_to_client)
                socket_to_client.flush()

                commando = pickle.load(socket_to_client)

            elif commando == "REGISTREREN":
                gegevens = pickle.load(socket_to_client)
                read_obj = open(Gebruikers_path, mode="rb")
                gebruikers = pickle.load(read_obj)
                new_id = {"id":len(gebruikers) + 1}
                print(gegevens)
                print(new_id)
                gegevens["id"] = len(gebruikers) + 1
                gegevens = {**new_id,**gegevens}
                print(gegevens)
                # gebruikers.append(gegevens)
                # write_obj = open(Gebruikers_path, mode="wb")
                # pickle.dump(gebruikers, write_obj)
                # write_obj.close()

                commando = pickle.load(socket_to_client)

            elif commando == "GET_BY_DATE":
                s1 = pickle.load(socket_to_client)  # SOM-object

                data = self.between("date",s1["start_date"], s1["end_date"])
                pickle.dump(data, socket_to_client)
                socket_to_client.flush()
                commando = pickle.load(socket_to_client)

            elif commando == "GET_BY_CLLIENT":
                data = self.customer()    

        self.print_bericht_gui_server("Connection with client closed...")
        self.socket_to_client.close()

    # def run(self):
    #     socket_to_client = self.socket_to_client.makefile(mode='rwb')

    #     self.print_bericht_gui_server("Waiting for numbers...")
    #     commando = pickle.load(socket_to_client)
    #     print(commando)

    #     while commando != "CLOSE":
    #         s1 = pickle.load(socket_to_client)  # SOM-object
    #         s1.som = s1.getal1 + s1.getal2
    #         pickle.dump(s1, socket_to_client)
    #         socket_to_client.flush()

    #         commando = pickle.load(socket_to_client)

    #     self.print_bericht_gui_server("Connection with client closed...")
    #     self.socket_to_client.close()

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")

    def between(self,unit,start,end):
        if unit == "date":
            result = df[df["Launch Date"].between(start,end)]
        elif unit == "weight":
            result = df[df["Payload Mass (kg)"].between(start,end)]

        return result

    def customer(self,customer_name):
        result = df[df['Customer Name']== customer_name]
        return result

