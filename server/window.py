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

        Label(self, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)

        
        #knop aanmaken
        startButton = Button(self,text="start server", height=1, command=self.startServer)
        stopButton = Button(self,text="stop server", height=1, command=self.stopServer )
        startButton.place(x=0,y=128)
        stopButton.place(x=0,y=160)


    def startServer(self):
        print('server starten')

    def stopServer(self):
        print('server stoppen')
