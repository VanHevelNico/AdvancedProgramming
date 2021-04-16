from tkinter import *

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()

    def init_window(self):
        #Titel van window instellen
        self.master.title("Eindopdracht Aaron Snauwaert & Nico Van Hevek")
        #Widget pakt volledige plek in
        self.pack(fill=BOTH,expand=1)

        #listbox met de logs
        Label(self, text="Logs server:").pack()
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        lstLogs = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=lstLogs.yview)


        #listbox met de ingelogde clients -> wanneer er op een item geklikt wordt moet de info van een client getoond worden (in een aparte window?)
        Label(self, text="Logged in clients:").pack()
        self.scrollbarLoggedIn = Scrollbar(self, orient=VERTICAL)
        lstLoggedIn = Listbox(self, yscrollcommand=self.scrollbarLoggedIn.set).pack()
        self.scrollbarLoggedIn.config(command=lstLogs.yview)
        list_items = [11,22,33,44,22,33,44,22,33,44,22,33,44,22,33,44,22,33,44]
        for item in list_items:
            lstLoggedIn.insert('end', item)
        lstLoggedIn.pack()
        lstLoggedIn.bind('<<ListboxSelect>>', showUserInfo)
        
        #knop aanmaken
        startButton = Button(self,text="Start server", height=1, command=self.startServer)
        stopButton = Button(self,text="Stop server", height=1, command=self.stopServer )
        startButton.pack()
        stopButton.pack()

    def showUserInfo(self):
        #haal de geklikte user op en toon in nieuw scherm
        lstLoggedIn.get(lstLoggedIn.curselection())

    def startServer(self):
        print('server starten')

    def stopServer(self):
        print('server stoppen')
