import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import requests

FT_LAT = 32.72541
FT_LON = -97.320847


account_sid = 'AC888d533566925a8ec989122942e7936a'
auth_token = os.environ.get("AUTH_TOKEN")
weather_api = os.environ.get("WEATHER_API")
client = Client(account_sid, auth_token)

parameters = {
    "appid": weather_api,
    "lat": FT_LAT,
    "lon": FT_LON,
    "exclude": "current,minutely,daily,alerts"
}

response = requests.get(url=f"https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()

lowest_code = 1000

for x in range(12):
    if response.json()["hourly"][x]["weather"][0]["id"] < lowest_code:
        lowest_code = response.json()["hourly"][x]["weather"][0]["id"]

msg = ""
if lowest_code <= 700:
    msg = "Bring an umbrella ☔️"

# Test Code
# elif lowest_code == 800:
#     msg = "Clear for the day 🌤"

if len(msg) > 0:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': ['https_proxy']}

    message = client.messages \
                    .create(
                         body=msg,
                         from_='TWILLIO_NUMBER',
                         to='MY_NUMBER'
                     )

    print(message.status)
