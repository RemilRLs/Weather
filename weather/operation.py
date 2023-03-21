import numpy as np
import numpy.ma as ma
import datetime as dt # I have to this because something went wrong.



class Operation:

    def __init__(self, dataset):
        self.dataset = dataset

    def getAverage(self, temp, dataset):
        vals = dataset.variables[temp][:]

        # We get the max average temperature in a year.

        # We calculate the average/mean for each day on the longitude and the latitude (that one was so hard to find).
        daily_avg = np.mean(vals, axis=(1, 2))

        # We get the index of the max temp average in a day.
        hottest_day = np.argmax(daily_avg)


        return hottest_day

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