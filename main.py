from weather.data_weather import Weather
from weather.data_visual import Visual

weather = Weather("resources/temperature/tmin.2020.nc", "resources/temperature/tmax.2020.nc", "resources/precipation/precip.2020.nc")
weather.open_weather_file()


visual = Visual(weather.dataset_tmin, weather.dataset_tmax, weather.dataset_prec, 54.0, 0.29)
visual.generate_visual_temperature()