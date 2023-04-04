from weather.data_weather import Weather
from weather.operation import Operation
from matplotlib.figure import Figure


import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.pylab as plt
import numpy as np
import numpy.ma as ma
import logging


class Visual:

    def __init__(self, data_tmin, data_tmax, data_prec, window):
        self.data_tmin = data_tmin
        self.data_tmax = data_tmax
        self.data_prec = data_prec
        self.tkwindow = window
        self.logger = logging.Logger("Visual")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)  # To handle the log.

    def generate_visual_temperature(self, lat_user, lon_user):

        weather = Weather()
        shortest_distance = 10000  # Default value
        lats = self.data_tmin.variables['lat'][:]
        lons = self.data_tmin.variables['lon'][:]
        vals_tmin = self.data_tmin.variables['tmin'][:]
        vals_tmax = self.data_tmax.variables['tmax'][:]

        vals_prec = self.data_prec.variables['precip'][:]

        mask = [[False] * len(lons) for _ in range(len(lats))]

        continuer = True

        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                if ma.is_masked(vals_tmin[0][i][j]):
                    mask[i][j] = True
                    continue

                km = weather.calcul_distance_coordinate(lat_user, lon_user, lat, lon)
                shortest_distance, coordinate = weather.shortest_distance_coordinate(lat, lon, km, shortest_distance)

                if coordinate != (0, 0):
                    real_coordinate = coordinate
                    pos = [i, j]
                if lon_user > 180:
                    lon_user = lon_user - 360
                break
            if not continuer:
                break
        print(shortest_distance, real_coordinate, pos)

        tmin_data = vals_tmin[:, pos[0], pos[1]]
        tmax_data = vals_tmax[:, pos[0], pos[1]]

        if len(tmin_data) == 366:
            tmin_data = tmin_data[:-1]
            tmax_data = tmax_data[:-1]

        prec_data = vals_prec[:, pos[0], pos[1]]

        if len(prec_data) == 366:
            prec_data = prec_data[:-1]

        fig = Figure(figsize=(15,6), frameon= True)
        gs = fig.add_gridspec(3,1)
        plot1 = fig.add_subplot(gs[0, 0])

        # Temperature Min and Max Curve.
        plot1.plot(range(1, 366), tmin_data, color='blue', label='Minimum Temperature')
        plot1.plot(range(1, 366), tmax_data, color='red', label='Maximum Temperature')
        plot1.set_title('Temperature')
        plot1.set_ylabel('Temperature (C)')
        plot1.legend()

        # Precipation Curve.

        plot2 = fig.add_subplot(gs[2, 0])

        plot2.plot(range(1, 366), prec_data, color='green', label='Precipitation')
        plot2.set_title('Precipitation')
        plot2.set_xlabel('Day')
        plot2.set_ylabel('Precipitation (mm)')
        plot2.legend()


        return fig




    def generate_map(self, day, temp):

        fig = plt.figure(figsize=(8,6), frameon=True)
        gs = fig.add_gridspec(3,1)



        if(temp == 'tmin'):
            lats = self.data_tmin.variables['lat'][:]
            lons = self.data_tmin.variables['lon'][:]
            vals = self.data_tmin.variables[temp][:]
        elif(temp == 'precip'):
            lats = self.data_prec.variables['lat'][:]
            lons = self.data_prec.variables['lon'][:]
            vals = self.data_prec.variables[temp][:]
        else:
            lats = self.data_tmax.variables['lat'][:]
            lons = self.data_tmax.variables['lon'][:]
            vals = self.data_tmax.variables[temp][:]

        if (temp == 'tmin' or temp == 'tmax'):

            ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
            c = ax.pcolormesh(lons, lats, vals[day], vmin=-10, vmax=40, transform=ccrs.PlateCarree(), cmap="jet", shading='auto')

            ax.coastlines(resolution='110m')
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.LAND.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'))
            fig.colorbar(c, ax=ax, fraction=0.046, pad=0.04)
        else:
            ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
            c = ax.pcolormesh(lons, lats, vals[day], vmin=0, vmax=20, transform=ccrs.PlateCarree(), cmap="jet", shading='auto')

            ax.coastlines(resolution='110m')
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.LAND.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'))
            fig.colorbar(c, ax=ax, fraction=0.046, pad=0.04)

        return fig

    def generate_map_month(self, start_month, end_month, temp):



        if(temp == 'tmin'):
            lats = self.data_tmin.variables['lat'][:]
            lons = self.data_tmin.variables['lon'][:]
            vals = self.data_tmin.variables[temp][:]
        elif(temp == 'precip'):
            lats = self.data_prec.variables['lat'][:]
            lons = self.data_prec.variables['lon'][:]
            vals = self.data_prec.variables[temp][:]
        else:
            lats = self.data_tmax.variables['lat'][:]
            lons = self.data_tmax.variables['lon'][:]
            vals = self.data_tmax.variables[temp][:]

        if(temp == 'tmin' or temp == 'tmax'):

            fig = plt.figure(figsize=(8,6), frameon=True)



            monthly_vals = np.mean(vals[start_month : end_month], axis= 0) # On fait la moyenne sur chaque jour des longitudes et des lattitudes. 2D Tab.


            ax = plt.subplot(111, projection=ccrs.PlateCarree())
            c = ax.pcolormesh(lons, lats, monthly_vals, vmin=-25, vmax=40, transform=ccrs.PlateCarree(), cmap="jet", shading='auto')

            ax.coastlines(resolution='110m');
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.LAND.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'))
            plt.colorbar(c, ax=ax, fraction=0.046, pad=0.04)
            plt.title("test")
        else:
            fig = plt.figure(figsize=(8,6), frameon=True)

            monthly_vals = np.mean(vals[start_month : end_month], axis= 0) # On fait la moyenne sur chaque jour des longitudes et des lattitudes. 2D Tab.


            ax = plt.subplot(111, projection=ccrs.PlateCarree())
            c = ax.pcolormesh(lons, lats, monthly_vals, vmin=0, vmax=20, transform=ccrs.PlateCarree(), cmap="jet", shading='auto')

            ax.coastlines(resolution='110m');
            ax.add_feature(cfeature.OCEAN.with_scale('50m'))
            ax.add_feature(cfeature.LAND.with_scale('50m'))
            ax.add_feature(cfeature.BORDERS.with_scale('50m'))
            plt.colorbar(c, ax=ax, fraction=0.046, pad=0.04)
            plt.title("test")

        return fig
