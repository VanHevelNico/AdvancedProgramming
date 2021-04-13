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

        Label(self, text="Logs server:").pack()
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        lstLogs = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=lstLogs.yview)
        list_items = [11,22,33,44,22,33,44,22,33,44,22,33,44,22,33,44,22,33,44]
        for item in list_items:
            lstLogs.insert('end', item)
        lstLogs.pack()

        
        #knop aanmaken
        startButton = Button(self,text="Start server", height=1, command=self.startServer)
        stopButton = Button(self,text="Stop server", height=1, command=self.stopServer )
        startButton.pack()
        stopButton.pack()


    def startServer(self):
        print('server starten')

    def stopServer(self):
        print('server stoppen')
