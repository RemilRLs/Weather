from netCDF4 import Dataset

import logging
import numpy as np
import math


class Weather:

    def __init__(self):
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

    def open_weather_file(self, p_path_file1, p_path_file2, p_path_file3):
        self.logger.debug("[#] - Loading data...")
        self.dataset_tmin = Dataset(p_path_file1, 'r')
        self.dataset_tmax = Dataset( p_path_file2, 'r')
        self.dataset_prec = Dataset(p_path_file3, 'r')
        self.logger.debug("[*] - Data loading complete.")



    def calcul_distance_coordinate(self, lat_1, lon_1, lat_2, lon_2):
        if lon_2 > 180:
            lon_2 = lon_2 - 360


        R = 6373.0  # Earth's radius in kilometers

        # We put everything in radian.

        lat_1_r = np.radians(lat_1)
        lon_1_r = np.radians(lon_1)
        lat_2_r = np.radians(lat_2)
        lon_2_r = np.radians(lon_2)

        # We calculate the difference between the two longitude and lattitude.

        dlon = lon_2_r - lon_1_r
        dlat = lat_2_r - lat_1_r

        a = np.sin(dlat / 2) ** 2 + np.cos(lat_1_r) * np.cos(lat_2_r) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

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

        if distance < shortest_distance:
            coordinate = (lat, lon)
            shortest_distance = distance
        else:
            coordinate = (0, 0)  # Default value for coordinate

        return shortest_distance, coordinate



