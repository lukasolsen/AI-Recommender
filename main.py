from tkinter import *
import customtkinter
import api


class Gui:
    def __init__(self):
        # Setting up a instance for the app and setting it's properties.
        self.app = customtkinter.CTk()
        self.app.geometry("800x480")
        self.app.title = "Recommender System"
        
    def work(self):
        # Creates a new (Input) for the user to type in their book.
        self.input = customtkinter.CTkEntry(self.app, placeholder_text="Enter the book you've read", width=1000)
        self.input.pack()
        
        # Creates a button that uses a command (run()) to run it.
        self.button = customtkinter.CTkButton(self.app, text="Check", command=self.run, width=1000)
        self.button.pack(pady=10)
        
    def run(self):
        # Used to run the API, and analyzing what books we get as recommendations (List).
        text = self.input.get()
        list = api.Api().run(text)
        
        # Looping through the list with recommended books.
        for T in list:
            # For each book, make a label (Text) to display the book.
            d = customtkinter.CTkLabel(self.app, text=T, width=1000)
            d.pack(pady=10)
        
        
        # EXAMPLE:          far beyond the stars (star trek deep space nine)
        
    def open(self):
        # Opens the GUI
        self.app.mainloop()

# Making it open when we run this file.
gui = Gui()
gui.work()
gui.open()