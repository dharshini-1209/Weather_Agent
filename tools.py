import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    """
    Returns the current weather for the given city.
    """

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return "Sorry, I couldn't find that city."

    data = response.json()

    city_name = data["name"]
    country = data["sys"]["country"]

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]

    weather = data["weather"][0]["description"]

    return (
        f"Weather in {city_name}, {country}\n"
        f"Condition : {weather}\n"
        f"Temperature : {temp}°C\n"
        f"Feels Like : {feels_like}°C\n"
        f"Humidity : {humidity}%"
    )


# -------------------------
# Test the function
# -------------------------
if __name__ == "__main__":
    print(get_weather("Chennai"))