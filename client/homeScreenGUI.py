from tkinter import *

class HomeScreenWindow(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Inloggen")
        self.pack( expand=1)

        Label(self, text="Naam").grid(row=0)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=1)
        
        Label(self, text="Nickname").grid(row=2)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=3)
                
        Label(self, text="Email").grid(row=4)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=5)

        self.buttonLogin = Button(self, text="Login", command=lambda: self.buttonInloggen(root))
        self.buttonLogin.grid(row=6, pady=(20, 10), padx=(5, 5), sticky=N + S + E + W)

        self.buttonRegister = Button(self, text="Registeren", command=self.buttonRegistreren)
        self.buttonRegister.grid(row=7, pady=(0, 10), padx=(5, 5), sticky=N + S + E + W)

        self.errorLabel = Label(self, text="")
        self.errorLabel.grid(row=8)


        Grid.rowconfigure(self, 8, weight=2)
        Grid.columnconfigure(self, 1, weight=1)

    def buttonInloggen(self, window):
        print("inloggen")

    def buttonRegistreren(self, window):
        print("inloggen")
