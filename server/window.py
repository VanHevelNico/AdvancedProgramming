from tkinter import *

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)               
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
        self.master = master
=======
>>>>>>> Stashed changes
        self.master = master
        self.init_window()

    def init_window(self):
        #Titel van window instellen
        self.master.title("Eindopdracht Aaron Snauwaert & Nico Van Hevek")
        #Widget pakt volledige plek in
        self.pack(fill=BOTH,expand=1)
        #knop aanmaken
        startButton = Button(self,text="start server")
<<<<<<< Updated upstream
        #stopButton = Button(self,Text="stop server")

        startButton.place(x=0,y=0)
=======
        stopButton = Button(self,text="stop server")
        startButton.place(x=0,y=0)
        stopButton.place(x=0,y=100)
>>>>>>> Stashed changes
>>>>>>> Stashed changes
