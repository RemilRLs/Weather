from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from weather.data_weather import Weather
from weather.operation import Operation
from weather.data_visual import Visual
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter import ttk


import tkinter as tk
import logging

class Visual_Tkinter:

    def __init__(self):
        self.selected_value = None
        self.list_day = None
        self.weather = Weather()
        self.window = ThemedTk(theme = "breeze")
        self.operation = Operation("a")
        self.main_window()





    def main_window(self):
        win = self.window
        win.title('PastWeather')
        win.resizable(width=False, height=False)
        win.geometry('1375x745')


        self.menu = tk.StringVar()
        self.menu.set("2020")

        self.list_day = self.operation.generate_date(2020, 1)

        list_menu = ttk.Notebook(win)
        list_menu.config(width=1350, height=745)
        list_menu.grid(row=2, column= 0, columnspan=50)

        self.local_frame_curve = tk.Frame(list_menu)
        self.global_frame_map = tk.Frame(list_menu)

        self.global_frame_map.grid( row=2, column= 1)

        list_menu.add(self.local_frame_curve, text='Local curve')
        list_menu.add(self.global_frame_map, text='Overall view')

        label_year = tk.Label(text='Year :')
        label_year.grid(row = 0, column = 0)


        # Loading Dropdown Menu.

        drop = tk.OptionMenu(win, self.menu, "2020", "2021", "2022")
        drop.grid(row = 0, column = 1)

        button = tk.Button(text='Load', command= self.get_year_user_choose)
        button.grid(row=0, column=2 )


        # Design Local Frame Curve.



        lat_label = tk.Label(self.local_frame_curve, text="Latitude :  ")
        lat_label.grid(row=0, column=1, sticky=tk.E)

        self.lat_entry = tk.Entry(self.local_frame_curve)
        self.lat_entry.grid(row=0, column=2, sticky=tk.E)

        lon_label = tk.Label(self.local_frame_curve, text="Longitude :  ")
        lon_label.grid(row=0, column=3, sticky=tk.E)

        self.lon_entry = tk.Entry(self.local_frame_curve)
        self.lon_entry.grid(row=0, column=4, sticky=tk.E, padx=10)

        self.display_button = tk.Button(self.local_frame_curve, text="Display", command=self.check_coordinates_and_generate)
        self.display_button.grid(row=0, column=5, sticky=tk.E)
        self.display_button.config(state=tk.DISABLED)



        self.local_frame_curve.columnconfigure(0, weight=1) # The column will take all the space to be center.
        self.local_frame_curve.columnconfigure(6, weight=1) # Same here.
        # Design Global Frame Map.

        self.selected_data_temp = tk.StringVar()
        self.selected_data_temp.set("Minimum Temperature")

        self.selected_data_maxmin = tk.StringVar()
        self.selected_data_maxmin.set("Minimum value")

        self.selected_date_day = tk.StringVar()
        self.selected_date_day.set("01")

        self.selected_date_month = tk.StringVar()
        self.selected_date_month.set("January")


        global_frame_menu = ttk.Notebook(self.global_frame_map)
        global_frame_menu.config(width=1350, height=745)
        global_frame_menu.grid(row=2, column= 0, columnspan=20)

        self.global_frame_page_day = tk.Frame(global_frame_menu)
        self.global_frame_page_month = tk.Frame(global_frame_menu)

        self.global_frame_page_day.grid(row = 0, column = 0)
        self.global_frame_page_month.grid(row = 0, column = 1)

        global_frame_menu.add(self.global_frame_page_day, text='Per day')
        global_frame_menu.add(self.global_frame_page_month, text='Per month')

        # Configure the columns to distribute the extra space
        self.global_frame_page_day.columnconfigure(0, weight=1)
        self.global_frame_page_day.columnconfigure(4, weight=1)

        self.global_frame_page_month.columnconfigure(0, weight=1)
        self.global_frame_page_month.columnconfigure(4, weight=1)

        label_data_day = tk.Label(self.global_frame_page_day, text='Data :')
        label_data_day.grid(row=0, column=0, sticky=tk.E)
        self.drop_data_temp = tk.OptionMenu(self.global_frame_page_day, self.selected_data_temp, "Minimum Temperature",
                                       "Maximum Temperature", "Precipitation")
        self.drop_data_temp.grid(row=0, column=2, sticky=tk.W)

        self.drop_data_temp.config(state=tk.DISABLED)

        # Choose a date.
        self.drop_data_day = tk.OptionMenu(self.global_frame_page_day, self.selected_date_day, *self.list_day)
        self.drop_data_day.grid(row=1, column=1, sticky=tk.E)
        self.drop_data_day.config(state=tk.DISABLED)

        label_character = tk.Label(self.global_frame_page_day, text='/')
        label_character.grid(row=1, column=2, sticky=tk.W)

        self.drop_data_month = tk.OptionMenu(self.global_frame_page_day, self.selected_date_month, "January", "February",
                                        "March", "April", "May", "June", "July", "August", "September", "October",
                                        "November", "December")
        self.drop_data_month.grid(row=1, column=2, sticky=tk.E)

        self.drop_data_month.config(state=tk.DISABLED)

        # Radio Button Configuration.
        self.selected_option_day = tk.StringVar()
        self.selected_option_day.set(0)

        self.option_date = tk.Radiobutton(self.global_frame_page_day, text='Precise Date : ', variable=self.selected_option_day,
                                     value='pre_dt')
        self.option_date.grid(row=1, column=0, sticky=tk.E)
        self.option_date.config(state=tk.DISABLED)



        self.option_other = tk.Radiobutton(self.global_frame_page_day, text='Other : ', variable=self.selected_option_day,
                                      value='other')
        self.option_other.grid(row=2, column=0, sticky=tk.E)

        self.option_other.config(state=tk.DISABLED)

        # Configuration Maximal and Minimal value.
        self.drop_data_maxmin = tk.OptionMenu(self.global_frame_page_day, self.selected_data_maxmin, "Minimum Value",
                                         "Maximal Value")
        self.drop_data_maxmin.grid(row=2, column=2, sticky=tk.W)
        self.drop_data_maxmin.config(state=tk.DISABLED)

        # Button Run Calculation.
        self.button = tk.Button(self.global_frame_page_day, text='Run', command=self.run_generate_map)
        self.button.grid(row=3, column=2, sticky=tk.W, pady=(15,0))
        self.button.config(state=tk.DISABLED)

        self.selected_date_month.trace('w', self.a)



        # Per Month Frame Design.

        label_data_day = tk.Label(self.global_frame_page_month, text='Data :')
        label_data_day.grid(row=0, column=0, sticky=tk.E)
        self.drop_data_temp_month_2 = tk.OptionMenu(self.global_frame_page_month, self.selected_data_temp, "Minimum Temperature",
                                       "Maximum Temperature", "Precipitation")
        self.drop_data_temp_month_2.grid(row=0, column=2, sticky=tk.W)
        self.drop_data_temp_month_2.config(state=tk.DISABLED)


        self.drop_data_month_2 = tk.OptionMenu(self.global_frame_page_month, self.selected_date_month, "January", "February",
                                        "March", "April", "May", "June", "July", "August", "September", "October",
                                        "November", "December")
        self.drop_data_month_2.grid(row=1, column=2, sticky=tk.E)
        self.drop_data_month_2.config(state=tk.DISABLED)


        self.selected_option = tk.StringVar()
        self.selected_option.set(0)

        self.option_date_month = tk.Radiobutton(self.global_frame_page_month, text='Precise Month : ', variable=self.selected_option,
                                     value='pre_month')
        self.option_date_month.grid(row=1, column=0, sticky=tk.E)
        self.option_date_month.config(state=tk.DISABLED)

        self.option_other_month = tk.Radiobutton(self.global_frame_page_month, text='Other : ', variable=self.selected_option,
                                      value='other')
        self.option_other_month.grid(row=2, column=0, sticky=tk.E)
        self.option_other_month.config(state=tk.DISABLED)

        # Configuration Maximal and Minimal value.
        self.drop_data_maxmin_month = tk.OptionMenu(self.global_frame_page_month, self.selected_data_maxmin, "Minimum Value",
                                         "Maximal Value")
        self.drop_data_maxmin_month.grid(row=2, column=2, sticky=tk.W)
        self.drop_data_maxmin_month.config(state=tk.DISABLED)

        # Button Run Calculation.
        self.button_month = tk.Button(self.global_frame_page_month, text='Run', command=self.run_generate_map_monthly)
        self.button_month.grid(row=3, column=2, sticky=tk.W, pady=(15,0))
        self.button_month.config(state=tk.DISABLED)

        win.mainloop()

    def get_year_user_choose(self):
        self.selected_value = self.menu.get()


        p_path_file1 = "resources/temperature/tmin." + self.selected_value + ".nc" # Min Temp
        p_path_file2 = "resources/temperature/tmax." + self.selected_value + ".nc" # Max Temp
        p_path_file3 = "resources/precipation/precip." + self.selected_value + ".nc" # Prec

        self.weather.open_weather_file(p_path_file1, p_path_file2, p_path_file3)

        self.display_button.config(state=tk.NORMAL)
        self.option_date.config(state=tk.NORMAL)
        self.drop_data_month.config(state=tk.NORMAL)
        self.drop_data_temp.config(state=tk.NORMAL)
        self.option_other.config(state=tk.NORMAL)
        self.drop_data_maxmin.config(state=tk.NORMAL)
        self.button.config(state=tk.NORMAL)
        self.drop_data_day.config(state=tk.NORMAL)
        self.drop_data_month.config(state=tk.NORMAL)
        self.drop_data_temp_month_2.config(state=tk.NORMAL)
        self.option_date_month.config(state=tk.NORMAL)
        self.drop_data_month_2.config(state=tk.NORMAL)
        self.option_other_month.config(state=tk.NORMAL)
        self.button_month.config(state=tk.NORMAL)
        self.drop_data_maxmin_month.config(state=tk.NORMAL)


    def check_coordinates_and_generate(self):
        lat = self.lat_entry.get()
        lon = self.lon_entry.get()

        if (not lat.replace(".", "").isdigit() and not lat.replace("-", "")) or (not lon.replace(".", "").isdigit() and not lat.replace("-", "")):
            messagebox.showerror("Error", "Please enter valid numeric values for Latitude and Longitude.")
        else:
            lat_value = float(lat)
            lon_value = float(lon)
            print(f"Latitude: {lat_value}, Longitude: {lon_value}")


            # We generate the local curve.
            visual = Visual(self.weather.dataset_tmin, self.weather.dataset_tmax, self.weather.dataset_prec, self.window)
            fig = visual.generate_visual_temperature(lat_value, lon_value)
            canvas = FigureCanvasTkAgg(fig, self.local_frame_curve)
            canvas = canvas.get_tk_widget()
            canvas.grid(row=1, column=0, columnspan=20)




    def display_date(self, month,):
        operation = Operation("a")

        month_nb = operation.month_to_num(month)

        return month_nb


    def a(self, name, index, mode):
        op = Operation("a")
        self.list_day = op.generate_date(int(self.menu.get()), self.display_date(self.selected_date_month.get()))
        self.update_dropdown_day()

    def update_dropdown_day(self):
        self.drop_data_day['menu'].delete(0, 'end') # We reset the dropdown menu.

        # We update the dropdown.
        for day in self.list_day:
            self.drop_data_day['menu'].add_command(label = day,command=tk._setit(self.selected_date_day, day))
        self.selected_date_day.set(self.list_day[0])

    def run_generate_map(self):
        visual = Visual(self.weather.dataset_tmin, self.weather.dataset_tmax, self.weather.dataset_prec, self.window)
        self.logger = logging.Logger("Tkinter")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

        self.logger.debug("[#] - Generating the map...")

        if(self.selected_data_temp.get() == "Minimum Temperature"):
            choice_temp = 'tmin'
        else: # Maximum Temperature.
            choice_temp = 'tmax'


        # We check the choice of the user.

        if(self.selected_option_day.get() == 'pre_dt'):

            # We get the number of day.

            number_day = self.operation.get_number_day(self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get())
            self.logger.debug("[INFO] - Day number : {0}".format(number_day))

            if(choice_temp == "precip"): # We need to change the message because that not the same than the temperature.
                self.logger.debug("[INFO] - You choose {0}".format(choice_temp))
            else:

                self.logger.debug("[INFO] - Temperature : {0}".format(choice_temp))

            # We generate the map.
            fig = visual.generate_map(number_day, choice_temp)
            canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
            canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
        else:
            maxmin_input = self.selected_data_maxmin.get()
            if(choice_temp == 'tmin'):

                if(maxmin_input == 'Minimum Value'):

                    self.logger.debug("[INFO] - Get the Coldest Day in Earth this Year...")

                    number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_tmin)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp)
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    self.logger.debug("[INFO] - Get the Hotest Day in Earth this Year...")

                    number_day = self.operation.getAverage_max(choice_temp, self.weather.dataset_tmin)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp)
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)

            else:

                if(maxmin_input == 'Minimum Value'):

                    self.logger.debug("[INFO] - Get the Coldest Day in Earth this Year...")

                    number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_tmax)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp)
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    self.logger.debug("[INFO] - Get the Hotest Day in Earth this Year...")

                    number_day = self.operation.getAverage_max(choice_temp, self.weather.dataset_tmax)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp)
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)


    def run_generate_map_monthly(self):
        visual = Visual(self.weather.dataset_tmin, self.weather.dataset_tmax, self.weather.dataset_prec, self.window)
        self.logger = logging.Logger("Tkinter")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

        self.logger.debug("[#] - Generating the map...")

        if(self.selected_data_temp.get() == "Minimum Temperature"):
            choice_temp = 'tmin'
        elif(self.selected_data_temp.get() == "Maximum Temperature"):
            choice_temp = 'tmax'
        else: # Precipitation.
            choice_temp = 'precip'

        # We check the choice of the user.

        if (self.selected_option.get() == 'pre_month'):

            # We get the number of day.

            self.logger.debug("[INFO] - Month  : {0}".format(self.selected_date_month.get()))
            self.logger.debug("[INFO] - Temperature : {0}".format(choice_temp))

            start_day_month = self.operation.get_number_day(1, self.selected_date_month.get(), self.menu.get())
            number_day = self.operation.return_day_in_month(int(self.menu.get()),self.selected_date_month.get())  # We get the number of day in this month and now we can slice the tab.
            end_day_month = start_day_month + number_day

            fig = visual.generate_map_month(start_day_month, end_day_month, choice_temp)
            canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
            canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
        else:
            maxmin_input = self.selected_data_maxmin.get()
            if (choice_temp == 'tmin'):

                if (maxmin_input == 'Minimum Value'):

                    self.logger.debug("[INFO] - Get the Coldest Day in Earth this Year...")

                    number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_tmin)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp)
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    self.logger.debug("[INFO] - Get the Hotest Day in Earth this Year...")

                    number_day = self.operation.getAverage_max(choice_temp, self.weather.dataset_tmin)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp)
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)

            else:

                if (maxmin_input == 'Minimum Value'):
                    if(choice_temp == "precip"):
                        self.logger.debug("[INFO] - Get the day with the least rain...")

                        number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_prec)

                        self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                        fig = visual.generate_map(number_day, choice_temp)
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                    else:
                        self.logger.debug("[INFO] - Get the Coldest Day in Earth this Year...")

                        number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_tmax)

                        self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                        fig = visual.generate_map(number_day, choice_temp)
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    if(choice_temp == "precip"):
                        self.logger.debug("[INFO] - Get the day with the most rain...")

                        number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_prec)

                        self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                        fig = visual.generate_map(number_day, choice_temp)
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                    else:
                        self.logger.debug("[INFO] - Get the Hotest Day in Earth this Year...")
    
                        number_day = self.operation.getAverage_max(choice_temp, self.weather.dataset_tmax)

                        self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                        fig = visual.generate_map(number_day, choice_temp)
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)





