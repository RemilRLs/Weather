import numpy as np
import numpy.ma as ma
import datetime as dt # I have to this because something went wrong.



class Operation:

    def __init__(self, dataset):
        self.dataset = dataset

    def getAverage_max(self, temp, dataset):
        vals = dataset.variables[temp][:]

        # We get the max average temperature in a year.

        # We calculate the average/mean for each day on the longitude and the latitude (that one was so hard to find).
        daily_avg = np.mean(vals, axis=(1, 2))

        # We get the index of the max temp average in a day.
        hotest_day = np.argmax(daily_avg)


        return hotest_day

    def getAverage_min(self, temp, dataset):
        vals = dataset.variables[temp][:]

        # We get the min average temperature in a year.

        # We calculate the average/mean for each day on the longitude and the latitude (that one was so hard to find).
        daily_avg = np.mean(vals, axis=(1, 2))

        # We get the index of the min temp average in a day.
        coldest_day = np.argmin(daily_avg)


        return coldest_day

    def get_average_month_min(self, temp, dataset, year):
        vals = dataset.variables[temp][:]

        tmp = 50.0



        for i in range (1, 12):

            number_day_begin_month = self.get_number_day_min_max(i, year)
            day_in_month = self.return_day_in_month_minmax(year, i)

            vals_month = vals[number_day_begin_month : (number_day_begin_month + day_in_month)]
            monthly_avg = np.mean(vals_month, axis=(1,2))

            min_month = min(monthly_avg)


            if(min_month < tmp):
                tmp = min_month
                month = i
                tuple_coordonate_month_min = (number_day_begin_month, (number_day_begin_month + day_in_month))

        return tuple_coordonate_month_min, month

    def get_average_month_max(self, temp, dataset, year):
        vals = dataset.variables[temp][:]

        tmp = 0.0

        for i in range(1, 12):

            number_day_begin_month = self.get_number_day_min_max(i, year)
            day_in_month = self.return_day_in_month_minmax(year, i)

            vals_month = vals[number_day_begin_month: (number_day_begin_month + day_in_month)]
            monthly_avg = np.mean(vals_month, axis=(1, 2))

            max_month = max(monthly_avg)

            if (max_month > tmp):
                tmp = max_month
                month = i
                tuple_coordonate_month_max = (number_day_begin_month, (number_day_begin_month + day_in_month))

        return tuple_coordonate_month_max, month

    def generate_date(self, year, month):

        nb_day = 365
        list_day = list()

        # Leap year.

        if (year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
            nb_day = 366

        date = dt.date(year, 1 , 1)
        deltat = dt.timedelta(days = 1)

        for _ in range(0, nb_day):
            date += deltat

            # We only want the day of the month.

            if(date.strftime("%m").replace('0', '') == str(month)):
                list_day.append(date.strftime("%d"))



        list_day_withouth_duplicate = self.remove_duplicate(list_day)

        return list_day_withouth_duplicate

    """
        Give us the month number (We use a dictionary method)
        
        Args:
            month : The month, ex : February.
        
        Returns:
            The month in number here 2 with February.
    """


    def month_to_num(self, month):
        return {
                'January': 1,
                'February': 2,
                'March': 3,
                'April': 4,
                'May': 5,
                'June': 6,
                'July': 7,
                'August': 8,
                'September': 9,
                'October': 10,
                'November': 11,
                'December': 12
        }[month]

    def num_to_month(self, num):
        return {
                1 : "January",
                2 : "February",
                3 : "March",
                4 : "April",
                5 : "May",
                6 : "June",
                7 : "July",
                8 : "August",
                9 : "September",
                10 : "October",
                11 : "November",
                12 : "December"
        }[num]

    """
        Function to remove duplicate.

        Args:
            list_day : A list that contain a list of day.

        Returns:
            The list of day without duplicate.
    """

    def remove_duplicate(self, list_day):

        my_dict = {}

        for item in list_day:
            my_dict[item] = None

        list_day_withouth_duplicate = list(my_dict.keys())

        return list_day_withouth_duplicate


    def get_number_day(self, day, month, year):
        user_date = dt.date(int(year), self.month_to_num(month), int(day))


        # We get the number of the day in a specific year.

        number_day = user_date.toordinal() - dt.date(user_date.year, 1, 1).toordinal() + 1

        return number_day

    def return_day_in_month(self, year, month):

        nub_month = self.month_to_num(month)

        if(nub_month != 12):
            day = (dt.date(year, nub_month + 1, 1) - dt.date(year, nub_month, 1)).days
        else: # If it's december we go to the next year.
            day = (dt.date(year + 1, 1, 1) - dt.date(year, nub_month, 1)).days

        return day

    def get_number_day_min_max(self, month, year):
        user_date = dt.date(int(year), month, 1)

        # We get the number of the day in a specific year.

        number_day = user_date.toordinal() - dt.date(user_date.year, 1, 1).toordinal() + 1

        return number_day

    def return_day_in_month_minmax(self, year, month):

        day = (dt.date(int(year), month + 1, 1) - dt.date(int(year), month, 1)).days


        return day