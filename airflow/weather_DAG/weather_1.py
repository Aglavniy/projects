import os
import requests
from dotenv import load_dotenv
import pandas as pd


def fetch_weather(api_key: str, city="Moscow") -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


if __name__ == "__main__":
    # test weather API
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    print(api_key)
    city = "Moscow"
    data = fetch_weather(api_key=api_key, city=city)
    print(data)


def add_row(city="Moscow", csv_name='weather.csv'):
    """Добавление строки в csvfile."""

    # read weather-csv
    df = pd.read_csv(csv_name)

    # load api_key from env
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    print(api_key)
    # load API data
    dict_weather = fetch_weather(api_key=api_key, city=city)

    # prepare row for concat
    new_row = {
        'datetime': dict_weather['dt'],
        'city': dict_weather['name'],
        'weather_main': dict_weather['weather'][0]['main'],
        'weather_description': dict_weather['weather'][0]['description'],
        'temp': dict_weather['main']['temp'],
        'feels_like': dict_weather['main']['feels_like'],
        'pressure': dict_weather['main']['pressure'],
        'wind_speed': dict_weather['wind']['speed'],

    }

    # add row
    df = pd.concat([
            df if not df.empty else None,
            pd.DataFrame([new_row])
                ], axis=0)

    # save new df
    df.to_csv(csv_name, index=False)


def only_col(csv_name='weather.csv') -> None:
    """Удаление строк в csvfile."""

    df = pd.read_csv(csv_name)
    df = pd.DataFrame([], columns=df.columns)
    df.to_csv(csv_name, index=False)


# add_row()
# only_col()
