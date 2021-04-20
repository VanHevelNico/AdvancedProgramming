import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

import os
sys.path[0] = str(Path(sys.path[0]).parent)
folder = os.path.dirname(os.path.abspath(__file__))
gebruikers_file = os.path.join(folder,'database/gebruikers.txt')
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
        def WriteToFile(data, file):
            write_obj = open(file, mode="wb")
            pickle.dump(data, write_obj)
            write_obj.close()
        
        def ReadFromFile(file):
            read_obj = open(file, mode="rb")
            return pickle.load(read_obj)

        def AddSearchToFile(zoekopdracht):
            # Zoekopdrachten opvragen
            zoekopdrachten = ReadFromFile(zoekopdrachten_file)
            # Zoekopdracht toeveoegen aan list
            zoekopdrachten.append(zoekopdracht)       
            # Scrijven naar zoekopdrachte file
            WriteToFile(zoekopdrachten,zoekopdrachten_file)

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
                # Boolean om te controleren of objecten gelrijk zijn
                same = False

                # De doorgestuurde gegevens van client inlezen
                gegevens = pickle.load(socket_to_client)
                print(gegevens)

                #Object maken van persoonsklasse voor in te loggen client
                gegevens_obj = Persoon(gegevens['name'],gegevens['nickname'],gegevens['email'])

                # Gebruikersfile inlezen
                gebruikers = ReadFromFile(gebruikers_file)

                # Controleren of gegevens al eens voorkomen in de dict via objecten
                for gebruiker in gebruikers:
                    #Object maken van persoonsklasse voor gebruiker
                    gebruiker_obj = Persoon(gebruiker['name'],gebruiker['nickname'],gebruiker['email'])
                    if (gebruiker_obj == gegevens_obj) == True:
                        same = True
                        gebruiker['isonline'] = 1
                # Indien er een overeenkomst is
                if same == True:
                    print("OK")
                    # Stuur OK naar client
                    pickle.dump("OK", socket_to_client)
                    socket_to_client.flush()
                elif same == False:
                    print("NOK")
                    # NOK sturen naar client
                    pickle.dump("NOK", socket_to_client)
                    socket_to_client.flush()
                print(gebruikers)
                #schrijven naar bestand
                WriteToFile(gebruikers, gebruikers_file)

                # Commando resetten
                commando = pickle.load(socket_to_client)

            


            elif commando == "REGISTREREN":
                # Boolean om te controleren of objecten gelrijk zijn
                same = False

                # De doorgestuurde gegevens van client inlezen
                gegevens = pickle.load(socket_to_client)

                #Object maken van persoonsklasse voor in te loggen client
                gegevens_obj = Persoon(gegevens['name'],gegevens['nickname'],gegevens['email'])

                # Gebruikersfile inlezen
                gebruikers = ReadFromFile(gebruikers_file)

                # Controleren of gegevens al eens voorkomen in de dict via objecten
                for gebruiker in gebruikers:
                    gebruiker_obj = Persoon(gebruiker['name'],gebruiker['nickname'],gebruiker['email'])
                    if (gebruiker_obj == gegevens_obj) == True:
                        same = True
                # Indien er al een account bestaat -> "Er is een account gevonden" naar client sturen
                if same:
                    pickle.dump("Een account  met deze gegevens bestaat al", socket_to_client)
                    socket_to_client.flush()

                # Anders nieuwe gebruiker toeveoegen
                else:
                    # Id toeveogen aan nieuwe
                    new_id = {"id":len(gebruikers) + 1}
                    gegevens = {**new_id,**gegevens}

                    # Nieuwe gebruiker toeveoegen aan de dict
                    gebruikers.append(gegevens)

                    #schrijven naar bestand
                    WriteToFile(gebruikers,gebruikers_file)

                    # Berichtt sturen naar client dat de gebruiker is geregistreerd
                    pickle.dump("Uw account werd aangemaakt", socket_to_client)
                    socket_to_client.flush()

                commando = pickle.load(socket_to_client)

            elif commando == "BETWEEN":
                soort = pickle.load(socket_to_client)
                gegevens = pickle.load(socket_to_client)
                value1 = gegevens['value1']
                value2 = gegevens['value2']

                if soort == "DATE":
                    # Zoekopdracht formateren
                    zoekopdracht = f'Lanceringen tussen {value1} en {value2}'
                    data = df[df["Launch Date"].between(value1,value2)]
                elif soort == "CARGO":
                    zoekopdracht = f'Lanceringen met een cargo tussen {value1}kg en {value2}kg'
                    data = df[df["Payload Mass (kg)"].between(int(value1),int(value2))]
                AddSearchToFile(zoekopdracht)
                pickle.dump(data, socket_to_client)
                socket_to_client.flush()

                # Reset commando
                commando = pickle.load(socket_to_client)

            elif commando == "FILL_COMBOBOX":
                data = df["Customer Name"].unique()
                pickle.dump(data, socket_to_client)
                socket_to_client.flush()
                commando = pickle.load(socket_to_client)

            elif commando == "GET_BY_CUSTOMER":
                customer_name = pickle.load(socket_to_client) 
                result = df[df['Customer Name']== customer_name]
                pickle.dump(result, socket_to_client)
                socket_to_client.flush()

                # Zoekopdracht formateren
                zoekopdracht = f'Lanceringen in opdracht van {customer_name}'

                # Zoekopdracht toeveoegen aan file
                AddSearchToFile(zoekopdracht)

                commando = pickle.load(socket_to_client)

            elif commando == "GET_GRAPH":
                launch_year = df
                result = launch_year.to_dict()
                pickle.dump(result, socket_to_client)
                socket_to_client.flush()

                soort = pickle.load(socket_to_client)
                # Zoekopdracht formateren
                zoekopdracht = f'Grafiek van lanceringen per {soort}'
                print(zoekopdracht)

                # Zoekopdracht toeveoegen aan file
                AddSearchToFile(zoekopdracht)

                commando = pickle.load(socket_to_client)


        # Ggevens opvangen
        login = pickle.load(socket_to_client)
        print(login)
        if login != "NOLOGIN":
            login_obj = Persoon(login['name'],login['nickname'],login['email'])

            # Gebruikersfile inlezen
            gebruikers = ReadFromFile(gebruikers_file)

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
            WriteToFile(gebruikers,gebruikers_file)

            print("------------------------- logout ------------------------- \n"+ str(gebruikers))
        
        # connectie sluiten
        print("before close connection")
        self.print_bericht_gui_server("Connection with client closed...")
        self.socket_to_client.close()

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")

    # def between(self,unit,start,end):
    #     if unit == "DATE":
    #         # Zoekopdracht formateren
    #         zoekopdracht = f'Lanceringen tussen {start} en {end}'
    #         result = df[df["Launch Date"].between(start,end)]

    #     elif unit == "CARGO":
    #         zoekopdracht = f'Lanceringen tussen {start}kg en {end}kg'
    #         result = df[df["Payload Mass (kg)"].between(start,end)]
    #     AddSearchToFile(zoekopdracht)
    #     return result

    def customer(self,customer_name):
        result = df[df['Customer Name']== customer_name]
        return result

