import tkinter as tk

class Visual_Tkinter:

    def __init__(self, window):
        self.window = window
        self.main_window()


    def main_window(self):
        win = self.window
        win.geometry('800x200')



        menu = tk.StringVar()
        menu.set("Select a year")

        drop = tk.OptionMenu(win, menu, "2020")
        drop.grid(row = 1, column = 1)

        button = tk.Button(text='Load')
        button.grid(row=1, column=2 ,padx=15)

        win.mainloop()
