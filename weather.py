import os
import dotenv
import requests

# Load Environment Variables (config.env)
dotenv.load_dotenv(dotenv_path="./config.env")


class Weather:
    def __init__(self, api):
        """
        Weather Module

        get_today_condition() -> str = Return today weather condition whether today is rainy or sunny day.
        get_today_uv_index() -> int = Return today weather UV Index.

        Parameters
        ----------
        api
        """
        self.api = api
        self.weather_region = os.getenv('WEATHER_LOCATION_REGION')
        self.forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={self.api}&q={self.weather_region}&days=1&aqi=no&alerts=no"
        # With this variable in __init__(self), the script doesn't need to request the content to the server every
        # single time which improve the program speed, response, and effectively reducing the weather api server load.
        self.forecast_source_data = requests.get(self.forecast_url)

    def get_today_condition(self) -> str:
        """
        Get today condition.

        Returns
        -------
        String:
        Moderate Rain, Thunderstorm, Sunny.
        """
        source = self.forecast_source_data.json()
        # * Like, Moderate Rain, Thunderstorm, or Sunny.
        return source["forecast"]["forecastday"][0]["day"]["condition"]["text"];

    def get_today_uv_index(self) -> int:
        """
        Get today UV Index.

        Returns
        -------
        UV Index ( INT )
        """
        source = self.forecast_source_data.json()
        # * Last time I saw is 11.0 UV Index
        return source["forecast"]["forecastday"][0]["day"]["uv"]


"""
For Testing...
Will get removed after the testing is finished.
"""
weather = Weather(os.getenv("WEATHER_API"))
