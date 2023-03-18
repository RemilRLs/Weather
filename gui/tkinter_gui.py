from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from weather.data_weather import Weather
from weather.data_visual import Visual
from tkinter import messagebox
from tkinter import ttk

import tkinter as tk

import os

class Visual_Tkinter:

    def __init__(self):
        self.selected_value = None
        self.weather = Weather()
        self.window = tk.Tk()
        self.main_window()



    def main_window(self):
        win = self.window
        win.title('PastWeather')
        win.geometry('800x200')


        self.menu = tk.StringVar()
        self.menu.set("Select a year")

        list_menu = ttk.Notebook(win)
        list_menu.grid(row=2, column= 0, columnspan=20)

        self.local_frame_curve = tk.Frame(list_menu)
        global_frame_map = tk.Frame(list_menu)

        self.local_frame_curve.grid( row=2, column= 0)
        global_frame_map.grid( row=2, column= 1)

        list_menu.add(self.local_frame_curve, text='Local curve')
        list_menu.add(global_frame_map, text='Overall view')

        label = tk.Label(text='Year : ')
        label.grid(row = 0, column = 0)

        drop = tk.OptionMenu(win, self.menu, "2020", "2021", "2022")
        drop.grid(row = 0, column = 1)

        button = tk.Button(text='Load', command= self.get_year_user_choose)
        button.grid(row=0, column=2 )


        lat_label = tk.Label(self.local_frame_curve, text="Latitude:")
        lat_label.grid(row=0, column=0)
        self.lat_entry = tk.Entry(self.local_frame_curve)
        self.lat_entry.grid(row=0, column=1)

        lon_label = tk.Label(self.local_frame_curve, text="Longitude:")
        lon_label.grid(row=0, column=2)
        self.lon_entry = tk.Entry(self.local_frame_curve)
        self.lon_entry.grid(row=0, column=3)

        display_button = tk.Button(self.local_frame_curve, text="Display", command=self.check_coordinates_and_generate)
        display_button.grid(row=0, column=4)

        win.mainloop()

    def get_year_user_choose(self):
        self.selected_value = self.menu.get()


        p_path_file1 = "resources/temperature/tmin." + self.selected_value + ".nc" # Min Temp
        p_path_file2 = "resources/temperature/tmax." + self.selected_value + ".nc" # Max Temp
        p_path_file3 = "resources/precipation/precip." + self.selected_value + ".nc" # Prec

        self.weather.open_weather_file(p_path_file1, p_path_file2, p_path_file3)


    def check_coordinates_and_generate(self):
        lat = self.lat_entry.get()
        lon = self.lon_entry.get()

        if not lat.replace(".", "").isdigit() or not lon.replace(".", "").isdigit():
            messagebox.showerror("Error", "Please enter valid numeric values for Latitude and Longitude.")
        else:
            lat_value = float(lat)
            lon_value = float(lon)
            print(f"Latitude: {lat_value}, Longitude: {lon_value}")


            # We generate the local curve.
            visual = Visual(self.weather.dataset_tmin, self.weather.dataset_tmax, self.weather.dataset_prec, lat_value, lon_value, self.window)
            fig = visual.generate_visual_temperature()
            canvas = FigureCanvasTkAgg(fig, self.local_frame_curve)
            canvas = canvas.get_tk_widget()
            canvas.grid(row=1, column=0, columnspan=20)


            #visual.generate_map()



    def load_year(self):
        print('a')