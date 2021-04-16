import threading

import pickle


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
        socket_to_client = self.socket_to_client.makefile(mode='rwb')

        self.print_bericht_gui_server("Waiting for numbers...")
        commando = pickle.load(socket_to_client)
        print(commando)

        while commando != "CLOSE":
            s1 = pickle.load(socket_to_client)  # SOM-object
            s1.som = s1.getal1 + s1.getal2
            pickle.dump(s1, socket_to_client)
            socket_to_client.flush()

            commando = pickle.load(socket_to_client)

        self.print_bericht_gui_server("Connection with client closed...")
        self.socket_to_client.close()

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
