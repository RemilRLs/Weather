from netCDF4 import Dataset

import logging
import math


class Weather:

    def __init__(self, p_path_file1, p_path_file2, p_path_file3):
        self.pathFile1 = p_path_file1
        self.pathFile2 = p_path_file2
        self.pathFile3 = p_path_file3
        self.logger = logging.Logger("Weather")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)  # To handle the log.

    """
        Load the data from the weather file.
        
        Args:
            None
        
        Returns:
            None
    """

    def open_weather_file(self):
        self.logger.debug("[#] - Loading data...")
        self.dataset_tmin = Dataset(self.pathFile1, 'r')
        self.dataset_tmax = Dataset(self.pathFile2, 'r')
        self.dataset_prec = Dataset(self.pathFile3, 'r')
        self.logger.debug("[*] - Data loading complete.")


    """
        Read the data from the weather data set file.

        Args:
            dataset: file that contain the data of the weather.

        Returns:
            None
    """

    def read_weather_file(self, dataset, type):

        shortest_distance = 5000 # Default value.

        lats = dataset.variables[type][:]
        lons = dataset.variables[type][:]
        times = dataset.variables[type][:]
        vals = dataset.variables[type][:]

        continuer = True



        #print(shortest_distance, real_coordinate)
    """
        Function to calculate km between two point (lat & lon)

        Args:
            lat_1: The lat where you are.
            lon_1: The lon where you are.
            lat_2: The lat that you going to compare.
            lon_2: The lon that you going to compare.

        Returns:
            distance: Distance in km between the two 2D coordinate.
    """

    def calcul_distance_coordinate(self, lat_1, lon_1, lat_2, lon_2):
        R = 6371.0  # Earth's radius in kilometers

        # We put everything in radian.

        lat_1_r = math.radians(lat_1)
        lon_1_r = math.radians(lon_1)
        lat_2_r = math.radians(lat_2)
        lon_2_r = math.radians(lon_2)

        # We calculate the difference between the two longitude and lattitude.

        dlon = lon_2_r - lon_1_r
        dlat = lat_2_r - lat_1_r

        a = math.sin(dlat / 2) ** 2 + math.cos(lat_1_r) * math.cos(lat_2_r) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c

        return distance

    """
        Function to calculate the shortest distance between two point.

        Args:
            lat: The lat where you are.
            lon: The lon where you are.
            distance: distance to compare
            shortest_distance: Default value.

        Returns:
            shortest_distance: The shortest distance.
            coordinate: Coordinate of where the shortest distance is.
    """

    def shortest_distance_coordinate(self, lat, lon, distance, shortest_distance):

        if shortest_distance > distance:
            coordinate = (lat, lon)
            shortest_distance = distance
        else:
            coordinate = (0, 0)  # Default value for coordinate

        return shortest_distance, coordinate



