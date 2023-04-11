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
        self.window = ThemedTk(theme = "adapta")
        self.operation = Operation("a")
        self.main_window()





    def main_window(self):
        win = self.window
        style = ttk.Style(self.window)
        style.theme_use("adapta")
        style.configure('Custom.TFrame', background='white')
        win.title('PastWeather')
        win.resizable(width=False, height=False)
        win.geometry('1375x850')



        self.menu = tk.StringVar()
        self.menu.set("Choose a year")

        self.list_day = self.operation.generate_date(2020, 1)

        list_menu = ttk.Notebook(win)
        list_menu.config(width=1350, height=745)
        list_menu.grid(row=2, column= 0, columnspan=50)

        self.local_frame_curve = ttk.Frame(list_menu, style='Custom.TFrame')
        self.global_frame_map = ttk.Frame(list_menu, style='Custom.TFrame')

        self.global_frame_map.grid( row=2, column= 1)

        list_menu.add(self.local_frame_curve, text='Local curve')
        list_menu.add(self.global_frame_map, text='Overall view')

        label_year = ttk.Label(text='Year :')
        label_year.grid(row = 0, column = 0)


        # Loading Dropdown Menu.

        drop = ttk.OptionMenu(win, self.menu, "Choose a year", "2010","2011","2012","2013","2014","2015","2016","2017","2018","2019", "2020", "2021", "2022")
        drop.grid(row = 0, column = 1)

        button = ttk.Button(text='Load', command= self.get_year_user_choose)
        button.grid(row=0, column=2 )


        # Design Local Frame Curve.



        lat_label = ttk.Label(self.local_frame_curve, text="Latitude :  ")
        lat_label.grid(row=0, column=1, sticky=tk.E)

        self.lat_entry = ttk.Entry(self.local_frame_curve)
        self.lat_entry.grid(row=0, column=2, sticky=tk.E)

        lon_label = ttk.Label(self.local_frame_curve, text="Longitude :  ")
        lon_label.grid(row=0, column=3, sticky=tk.E)

        self.lon_entry = ttk.Entry(self.local_frame_curve)
        self.lon_entry.grid(row=0, column=4, sticky=tk.E, padx=10)

        self.display_button = ttk.Button(self.local_frame_curve, text="Display", command=self.check_coordinates_and_generate)
        self.display_button.grid(row=0, column=5, sticky=tk.E)
        self.display_button.config(state=tk.DISABLED)



        self.local_frame_curve.columnconfigure(0, weight=1) # The column will take all the space to be center.
        self.local_frame_curve.columnconfigure(6, weight=1) # Same here.
        # Design Global Frame Map.

        self.selected_data_temp = tk.StringVar()
        self.selected_data_temp.set("Minimum Temperature")

        self.selected_data_maxmin = tk.StringVar()
        self.selected_data_maxmin.set("Minimum Value")

        self.selected_date_day = tk.StringVar()
        self.selected_date_day.set("Day")

        self.selected_date_month = tk.StringVar()
        self.selected_date_month.set("Choose a month")


        global_frame_menu = ttk.Notebook(self.global_frame_map)
        global_frame_menu.config(width=1350, height=745)
        global_frame_menu.grid(row=2, column= 0, columnspan=20)

        self.global_frame_page_day = ttk.Frame(global_frame_menu, style='Custom.TFrame')
        self.global_frame_page_month = ttk.Frame(global_frame_menu, style='Custom.TFrame')

        self.global_frame_page_day.grid(row = 0, column = 0)
        self.global_frame_page_month.grid(row = 0, column = 1)

        global_frame_menu.add(self.global_frame_page_day, text='Per day')
        global_frame_menu.add(self.global_frame_page_month, text='Per month')

        # Configure the columns to distribute the extra space
        self.global_frame_page_day.columnconfigure(0, weight=1)
        self.global_frame_page_day.columnconfigure(4, weight=1)

        self.global_frame_page_month.columnconfigure(0, weight=1)
        self.global_frame_page_month.columnconfigure(4, weight=1)

        label_data_day = ttk.Label(self.global_frame_page_day, text='Data :')
        label_data_day.grid(row=0, column=0, sticky=tk.E)
        self.drop_data_temp = ttk.OptionMenu(self.global_frame_page_day, self.selected_data_temp, "Choose type of Data", "Minimum Temperature",
                                       "Maximum Temperature", "Precipitation")
        self.drop_data_temp.grid(row=0, column=2, sticky=tk.W)

        self.drop_data_temp.config(state=tk.DISABLED)

        # Choose a date.
        self.drop_data_day = ttk.OptionMenu(self.global_frame_page_day, self.selected_date_day, *self.list_day)
        self.drop_data_day.grid(row=1, column=1, sticky=tk.E)
        self.drop_data_day.config(state=tk.DISABLED)

        label_character = ttk.Label(self.global_frame_page_day, text='/')
        label_character.grid(row=1, column=2, sticky=tk.W)

        self.drop_data_month = ttk.OptionMenu(self.global_frame_page_day, self.selected_date_month, "January","January", "February",
                                        "March", "April", "May", "June", "July", "August", "September", "October",
                                        "November", "December")
        self.drop_data_month.grid(row=1, column=2, sticky=tk.E)


        self.drop_data_month.config(state=tk.DISABLED)

        # Radio Button Configuration.
        self.selected_option_day = tk.StringVar()
        self.selected_option_day.set('Day')

        self.option_date = ttk.Radiobutton(self.global_frame_page_day, text='Precise Date : ', variable=self.selected_option_day,
                                     value='pre_dt')
        self.option_date.grid(row=1, column=0, sticky=tk.E)
        self.option_date.config(state=tk.DISABLED)



        self.option_other = ttk.Radiobutton(self.global_frame_page_day, text='Other : ', variable=self.selected_option_day,
                                      value='other')
        self.option_other.grid(row=2, column=0, sticky=tk.E)

        self.option_other.config(state=tk.DISABLED)

        # Configuration Maximal and Minimal value.
        self.drop_data_maxmin = ttk.OptionMenu(self.global_frame_page_day, self.selected_data_maxmin, "Value","Minimal Value",
                                         "Maximal Value")
        self.drop_data_maxmin.grid(row=2, column=2, sticky=tk.W)
        self.drop_data_maxmin.config(state=tk.DISABLED)

        # Button Run Calculation.
        self.button = ttk.Button(self.global_frame_page_day, text='Run', command=self.run_generate_map)
        self.button.grid(row=3, column=2, sticky=tk.W, pady=(15,0))
        self.button.config(state=tk.DISABLED)

        self.selected_date_month.trace('w', self.a)



        # Per Month Frame Design.

        label_data_day = ttk.Label(self.global_frame_page_month, text='Data :')
        label_data_day.grid(row=0, column=0, sticky=tk.E)
        self.drop_data_temp_month_2 = ttk.OptionMenu(self.global_frame_page_month, self.selected_data_temp, "Choose type of Data","Minimum Temperature",
                                       "Maximum Temperature", "Precipitation")
        self.drop_data_temp_month_2.grid(row=0, column=2, sticky=tk.W)
        self.drop_data_temp_month_2.config(state=tk.DISABLED)


        self.drop_data_month_2 = ttk.OptionMenu(self.global_frame_page_month, self.selected_date_month, "January","January", "February",
                                        "March", "April", "May", "June", "July", "August", "September", "October",
                                        "November", "December")
        self.drop_data_month_2.grid(row=1, column=2, sticky=tk.E)
        self.drop_data_month_2.config(state=tk.DISABLED)


        self.selected_option = tk.StringVar()
        self.selected_option.set(0)

        self.option_date_month = ttk.Radiobutton(self.global_frame_page_month, text='Precise Month : ', variable=self.selected_option,
                                     value='pre_month')
        self.option_date_month.grid(row=1, column=0, sticky=tk.E)
        self.option_date_month.config(state=tk.DISABLED)

        self.option_other_month = ttk.Radiobutton(self.global_frame_page_month, text='Other : ', variable=self.selected_option,
                                      value='other')
        self.option_other_month.grid(row=2, column=0, sticky=tk.E)
        self.option_other_month.config(state=tk.DISABLED)

        # Configuration Maximal and Minimal value.
        self.drop_data_maxmin_month = ttk.OptionMenu(self.global_frame_page_month, self.selected_data_maxmin,"Value" ,"Minimal Value",
                                         "Maximal Value")
        self.drop_data_maxmin_month.grid(row=2, column=2, sticky=tk.W)
        self.drop_data_maxmin_month.config(state=tk.DISABLED)

        # Button Run Calculation.
        self.button_month = ttk.Button(self.global_frame_page_month, text='Run', command=self.run_generate_map_monthly)
        self.button_month.grid(row=3, column=2, sticky=tk.W, pady=(15,0))
        self.button_month.config(state=tk.DISABLED)

        win.mainloop()

    def get_year_user_choose(self):

        try:
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
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the dataset: {str(e)}")


    def check_coordinates_and_generate(self):
        lat = self.lat_entry.get()
        lon = self.lon_entry.get()


        try:
            lat_value = float(lat)
            lon_value = float(lon)
            print(f"Latitude: {lat_value}, Longitude: {lon_value}")
            # We generate the local curve.
            visual = Visual(self.weather.dataset_tmin, self.weather.dataset_tmax, self.weather.dataset_prec, self.window)
            fig = visual.generate_visual_temperature(lat_value, lon_value)
            canvas = FigureCanvasTkAgg(fig, self.local_frame_curve)
            canvas = canvas.get_tk_widget()
            canvas.grid(row=1, column=0, columnspan=20)
        except Exception as e:
            messagebox.showerror("Error", "Please enter valid numeric values for Latitude and Longitude.")







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
        elif(self.selected_data_temp.get() == "Precipitation"):
            choice_temp= 'precip'
        elif (self.selected_data_temp.get() == "Maximum Temperature"): # Maximum Temperature.
            choice_temp = 'tmax'
        else:
            messagebox.showerror("Error", "You need to select the Data that you want.")
            return

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
            fig = visual.generate_map(number_day, choice_temp, self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get(),self.selected_data_maxmin.get(), self.selected_option_day.get())
            canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
            canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
        elif(self.selected_option_day.get() == 'other'):
            maxmin_input = self.selected_data_maxmin.get()

            if(choice_temp == 'tmin'):

                if(maxmin_input == 'Minimal Value'):

                    self.logger.debug("[INFO] - Get the Coldest Day in Earth this Year...")

                    number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_tmin)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp, self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get(), self.selected_data_maxmin.get(), self.selected_option_day.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                elif(maxmin_input == 'Maximal Value'):
                    self.logger.debug("[INFO] - Get the Hotest Day in Earth this Year...")

                    number_day = self.operation.getAverage_max(choice_temp, self.weather.dataset_tmin)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp, self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get(), self.selected_data_maxmin.get(), self.selected_option_day.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    messagebox.showerror("Error", "You need to select a Value in the section Other.")

            elif(choice_temp == 'precip'):
                if(maxmin_input == 'Minimal Value'):

                    self.logger.debug("[INFO] - Get the day with the least rain...")

                    number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_prec)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp, self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get(),self.selected_data_maxmin.get(), self.selected_option_day.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)

                elif(maxmin_input == "Maximal Value"):
                    self.logger.debug("[INFO] - Get the day with the most rain...")

                    number_day = self.operation.getAverage_max(choice_temp, self.weather.dataset_prec)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp, self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get(),self.selected_data_maxmin.get(), self.selected_option_day.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    messagebox.showerror("Error", "You need to select a Value in the section Other.")

            elif(choice_temp == 'tmax'):
                if(maxmin_input == 'Minimal Value'):

                    self.logger.debug("[INFO] - Get the Coldest Day in Earth this Year...")

                    number_day = self.operation.getAverage_min(choice_temp, self.weather.dataset_tmax)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp, self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get(),self.selected_data_maxmin.get(), self.selected_option_day.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                elif(maxmin_input == "Maximal Value"):
                    self.logger.debug("[INFO] - Get the Hotest Day in Earth this Year...")

                    number_day = self.operation.getAverage_max(choice_temp, self.weather.dataset_tmax)

                    self.logger.debug("[INFO] - Day number : {0}".format(number_day))

                    fig = visual.generate_map(number_day, choice_temp, self.selected_date_day.get(), self.selected_date_month.get(), self.menu.get(),self.selected_data_maxmin.get(), self.selected_option_day.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_day)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    messagebox.showerror("Error", "You need to select a Value in the section Other.")
        else:
            messagebox.showerror("Error", "You need to select an option (Precise Date or Other).")

    def run_generate_map_monthly(self):
        visual = Visual(self.weather.dataset_tmin, self.weather.dataset_tmax, self.weather.dataset_prec, self.window)
        self.logger = logging.Logger("Tkinter")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)
        op = Operation("a")

        self.logger.debug("[#] - Generating the map...")

        if(self.selected_data_temp.get() == "Minimum Temperature"):
            choice_temp = 'tmin'
        elif(self.selected_data_temp.get() == "Maximum Temperature"):
            choice_temp = 'tmax'
        elif(self.selected_data_temp.get() == "Precipation"): # Precipitation.
            choice_temp = 'precip'
        else:
            messagebox.showerror("Error", "You need to select the Data that you want.")
            return

        # We check the choice of the user.

        if (self.selected_option.get() == 'pre_month'):

            # We get the number of day.

            self.logger.debug("[INFO] - Month  : {0}".format(self.selected_date_month.get()))
            self.logger.debug("[INFO] - Temperature : {0}".format(choice_temp))

            start_day_month = self.operation.get_number_day(1, self.selected_date_month.get(), self.menu.get())
            number_day = self.operation.return_day_in_month(int(self.menu.get()),self.selected_date_month.get())  # We get the number of day in this month and now we can slice the tab.
            end_day_month = start_day_month + number_day

            fig = visual.generate_map_month(start_day_month, end_day_month, choice_temp, self.selected_date_month.get(), self.menu.get(), self.selected_option_day.get(), self.selected_option.get())
            canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
            canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
        elif(self.selected_option.get() == 'other'):
            maxmin_input = self.selected_data_maxmin.get()
            if (choice_temp == 'tmin'):

                if (maxmin_input == 'Minimal Value'):

                    self.logger.debug("[INFO] - Get the Coldest month in Earth this Year...")

                    coordinate_month, month = self.operation.get_average_month_min(choice_temp, self.weather.dataset_tmin, self.menu.get())

                    self.logger.debug("[INFO] - Month number : {0}".format(month))

                    fig = visual.generate_map_month(coordinate_month[0], coordinate_month[1], choice_temp, op.num_to_month(month), self.menu.get(), self.selected_option_day.get(), self.selected_option.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    self.logger.debug("[INFO] - Get the Hotest Day in Earth this Year...")
                    coordinate_month, month = self.operation.get_average_month_max(choice_temp, self.weather.dataset_tmin, self.menu.get())

                    self.logger.debug("[INFO] - Month number : {0}".format(month))

                    fig = visual.generate_map_month(coordinate_month[0], coordinate_month[1], choice_temp, op.num_to_month(month), self.menu.get(), self.selected_option_day.get(), self.selected_option.get())
                    canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                    canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
            else:

                if (maxmin_input == 'Minimal Value'):
                    if(choice_temp == "precip"):
                        self.logger.debug("[INFO] - Get the month with the least rain...")

                        coordinate_month, month = self.operation.get_average_month_min(choice_temp, self.weather.dataset_prec, self.menu.get())

                        self.logger.debug("[INFO] - Month number : {0}".format(month))

                        fig = visual.generate_map_month(coordinate_month[0], coordinate_month[1], choice_temp, op.num_to_month(month), self.menu.get(), self.selected_option_day.get(), self.selected_option.get())
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                    else:
                        self.logger.debug("[INFO] - Get the Coldest Month in Earth this Year...")

                        coordinate_month, month = self.operation.get_average_month_min(choice_temp, self.weather.dataset_tmax, self.menu.get())

                        self.logger.debug("[INFO] - Month number : {0}".format(month))

                        fig = visual.generate_map_month(coordinate_month[0], coordinate_month[1], choice_temp, op.num_to_month(month), self.menu.get(), self.selected_option_day.get(), self.selected_option.get())
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                elif(maxmin_input == 'Maximal Value'):
                    if(choice_temp == "precip"):
                        self.logger.debug("[INFO] - Get the month with the most rain...")

                        coordinate_month, month = self.operation.get_average_month_max(choice_temp, self.weather.dataset_prec, self.menu.get())

                        self.logger.debug("[INFO] - Month number : {0}".format(month))

                        fig = visual.generate_map_month(coordinate_month[0], coordinate_month[1], choice_temp, op.num_to_month(month), self.menu.get(), self.selected_option_day.get(), self.selected_option.get())
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                    else:
                        self.logger.debug("[INFO] - Get the Hotest Month in Earth this Year...")

                        coordinate_month, month = self.operation.get_average_month_max(choice_temp, self.weather.dataset_tmax, self.menu.get())

                        self.logger.debug("[INFO] - Month number : {0}".format(month))

                        fig = visual.generate_map_month(coordinate_month[0], coordinate_month[1], choice_temp, op.num_to_month(month), self.menu.get(), self.selected_option_day.get(), self.selected_option.get())
                        canvas = FigureCanvasTkAgg(fig, self.global_frame_page_month)
                        canvas.get_tk_widget().grid(row=4, column=0, columnspan=50)
                else:
                    messagebox.showerror("Error", "You need to select a Value in the section Other.")
        else:
            messagebox.showerror("Error", "You need to select an option (Precise Date or Other).")





