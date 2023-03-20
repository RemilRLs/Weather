import numpy.ma as ma
import numpy as np
import math
import matplotlib.pyplot as plt

class Operation:

    def __init__(self, dataset):
        self.dataset = dataset

    def getAverage(self):
        vals = self.dataset.variables['tmax'][:]

        # We get the max average temperature in a year.
        avg = np.mean(vals, axis=0)
        max_day = np.argmax(avg)
        day, remainder = divmod(max_day, 365)


        return day




