from weather.data_weather import Weather
from netCDF4 import Dataset
from weather.operation import Operation
import cartopy.feature as cfeature
import matplotlib as mpl
import cartopy.crs as ccrs

import matplotlib.pylab as plt
import numpy as np
import numpy.ma as ma
import logging


class Visual:

    def __init__(self, data_tmin, data_tmax, data_prec, lat, lon):
        self.data_tmin = data_tmin
        self.data_tmax = data_tmax
        self.data_prec = data_prec
        self.lat = lat
        self.lon = lon
        self.logger = logging.Logger("Visual")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)  # To handle the log.

    def generate_visual_temperature(self):

        weather = Weather("test", "test", "test")
        shortest_distance = 5000  # Default value
        lats = self.data_tmin.variables['lat'][:]
        lons = self.data_tmin.variables['lon'][:]
        vals_tmin = self.data_tmin.variables['tmin'][:]
        vals_tmax = self.data_tmax.variables['tmax'][:]

        vals_prec = self.data_prec.variables['precip'][:]

        avg = np.zeros((len(lats), len(lons)))
        mask = [[False] * len(lons) for _ in range(len(lats))]

        continuer = True

        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                if ma.is_masked(vals_tmin[0][i][j]):
                    mask[i][j] = True
                    continue
                km = weather.calcul_distance_coordinate(self.lat, self.lon + 360, lat, lon)
                shortest_distance, coordinate = weather.shortest_distance_coordinate(lat, lon, km, shortest_distance)

                if coordinate != (0, 0):
                    real_coordinate = coordinate
                    pos = [i, j]
                if lon > 180:
                    lon = lon - 360
                break
            if not continuer:
                break
        print(shortest_distance, real_coordinate, pos)

        tmin_data = vals_tmin[:, pos[0], pos[1]]
        tmin_data = tmin_data[:-1]

        tmax_data = vals_tmax[:, pos[0], pos[1]]
        tmax_data = tmax_data[:-1]

        prec_data = vals_prec[:, pos[0], pos[1]]
        prec_data = prec_data[:-1]


        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(range(1, 366), tmin_data, color='blue', label='Minimum Temperature')
        ax1.plot(range(1, 366), tmax_data, color='red', label='Maximum Temperature')
        ax1.set_title('Temperature')
        ax1.set_ylabel('Temperature (C)')
        ax1.legend()

        ax2.plot(range(1, 366), prec_data, color='green', label='Precipitation')
        ax2.set_title('Precipitation')
        ax2.set_xlabel('Day')
        ax2.set_ylabel('Precipitation (mm)')
        ax2.legend()


        plt.show()




    def generate_map(self):
        operation = Operation(self.data_tmax)

        day = operation.getAverage()

        lats = self.data_tmax.variables['lat'][:]

        lons = self.data_tmax.variables['lon'][:]

        vals = self.data_tmax.variables['tmax'][:]

        ax = plt.subplot(111, projection=ccrs.PlateCarree())
        c = ax.pcolormesh(lons, lats, vals[day], vmin=-25, vmax=25, transform=ccrs.PlateCarree(), cmap="jet")

        ax.coastlines(resolution='110m');
        ax.add_feature(cfeature.OCEAN.with_scale('50m'))
        ax.add_feature(cfeature.LAND.with_scale('50m'))
        ax.add_feature(cfeature.BORDERS.with_scale('50m'))
        plt.colorbar(c, ax=ax, fraction=0.046, pad=0.04)

        plt.show()