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
        #knop aanmaken
        startButton = Button(self,text="start server")
        #stopButton = Button(self,Text="stop server")

        startButton.place(x=0,y=0)
