import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

import os
sys.path[0] = str(Path(sys.path[0]).parent)
folder = os.path.dirname(os.path.abspath(__file__))
gebruikers_file = os.path.join(folder,'database/Gebruikers.txt')
database_file = os.path.join(folder,'database/database.csv')
zoekopdrachten_file = os.path.join(folder,'database/zoekopdrachten.txt')

import threading
import pickle

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from server.klassen.Persoon import Persoon

df = pd.read_csv(database_file)
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

        same = False
        socket_to_client = self.socket_to_client.makefile(mode='rwb')

        self.print_bericht_gui_server("Waiting for command...")
        commando = pickle.load(socket_to_client)
        print(commando)

        while commando != "CLOSE":
            if commando == "SOM":
                s1 = pickle.load(socket_to_client)  # SOM-object
                s1.som = s1.getal1 + s1.getal2
                pickle.dump(s1, socket_to_client)
                socket_to_client.flush()

                commando = pickle.load(socket_to_client)

            elif commando == "INLOGGEN":
                same = False
                gegevens = pickle.load(socket_to_client)
                gegevens_obj = Persoon(gegevens['name'],gegevens['nickname'],gegevens['email'])
                # Gebruikersfile inlezen
                read_obj = open(gebruikers_file, mode="rb")
                gebruikers = pickle.load(read_obj)

                # Controleren of gegevens al eens voorkomen in de dict via objecten
                for gebruiker in gebruikers:
                    gebruiker_obj = Persoon(gebruiker['name'],gebruiker['nickname'],gebruiker['email'])

                    if (gebruiker_obj == gegevens_obj) == True:
                        same = True
                        if same == True:
                            print("same")
                            pickle.dump("OK", socket_to_client)
                            gebruiker['isonline'] = 1

                            socket_to_client.flush()
                        else:
                            pickle.dump("NOK", socket_to_client)
                            print("NOK")
                            socket_to_client.flush()

                #schrijven naar bestand
                write_obj = open(gebruikers_file, mode="wb")
                pickle.dump(gebruikers, write_obj)
                write_obj.close()
                print("------------------------- login ------------------------- \n"+ str(gebruikers)+"\n\n\n\n\n")

                commando = pickle.load(socket_to_client)


            elif commando == "REGISTREREN":
                same = False
                gegevens = pickle.load(socket_to_client)
                print("gegevens" + str(gegevens))
                gegevens_obj = Persoon(gegevens['name'],gegevens['nickname'],gegevens['email'])
                # Gebruikersfile inlezen
                read_obj = open(gebruikers_file, mode="rb")
                gebruikers = pickle.load(read_obj)

                # Controleren of gegevens al eens voorkomen in de dict via objecten
                for gebruiker in gebruikers:
                    gebruiker_obj = Persoon(gebruiker['name'],gebruiker['nickname'],gebruiker['email'])
                    print(gebruiker)

                    if (gebruiker_obj == gegevens_obj) == True:
                        same = True
                        print("same")
                if same:
                    pickle.dump("Een account  met deze gegevens bestaat al", socket_to_client)
                    socket_to_client.flush()

                else:

                    # Id toeveogen aan nieuwe
                    new_id = {"id":len(gebruikers) + 1}
                    gegevens = {**new_id,**gegevens}

                    # Nieuwe gebruiker toeveoegen aan de dict
                    gebruikers.append(gegevens)

                    #schrijven naar bestand
                    write_obj = open(gebruikers_file, mode="wb")
                    pickle.dump(gebruikers, write_obj)
                    write_obj.close()

                    pickle.dump("Uw account werd aangemaakt", socket_to_client)
                    socket_to_client.flush()

                commando = pickle.load(socket_to_client)

            elif commando == "GET_BY_DATE":
                s1 = pickle.load(socket_to_client)  # SOM-object

                data = self.between("date",s1["start_date"], s1["end_date"])
                pickle.dump(data, socket_to_client)
                socket_to_client.flush()
                commando = pickle.load(socket_to_client)
                saveSearches(commando)

            elif commando == "GET_BY_CLLIENT":
                data = self.customer()    

        # Ggevens opvangen
        login = pickle.load(socket_to_client)
        print(login)
        if login != "NOLOGIN":
            login_obj = Persoon(login['name'],login['nickname'],login['email'])

            # Gebruikersfile inlezen
            read_obj = open(gebruikers_file, mode="rb")
            gebruikers = pickle.load(read_obj)

        # Controleren of gegevens al eens voorkomen in de dict via objecten
            for gebruiker in gebruikers:
                gebruiker_obj = Persoon(gebruiker['name'],gebruiker['nickname'],gebruiker['email'])
                if (gebruiker_obj == login_obj) == True:
                    same = True
                    if same == True:
                        print(gebruiker)
                        print("same")
                        gebruiker["isonline"] = 0

            #schrijven naar bestand
            write_obj = open(gebruikers_file, mode="wb")
            pickle.dump(gebruikers, write_obj)
            write_obj.close()
            print("------------------------- logout ------------------------- \n"+ str(gebruikers))
        
        # connectie sluiten
        self.print_bericht_gui_server("Connection with client closed...")
        pickle.dump("CLOSE", socket_to_client)
        self.socket_to_client.close()

    def saveSearches(self, com):
        gegevens_obj = com
        reader = open(zoekopdrachten_file, mode="rb")
        zoekopdrachten = pickle.load(reader)
        print(zoekopdrachten)
        # Nieuwe gebruiker toeveoegen aan de dict
        zoekopdrachten.append(gegevens_obj)
        #schrijven naar bestand
        write_obj = open(gebruikers_file, mode="wb")
        pickle.dump(zoekopdrachten, write_obj)
        write_obj.close()

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

