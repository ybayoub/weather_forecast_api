import requests
from twilio.rest import Client
import os

# ----------- Twilio setup ------------------
# Values to set with you own credentials/data (env or set directly into the code)
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
account_sid = os.environ.get("ACCOUNT_SID")
from_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
my_phone_number = os.environ.get("YOUR_PHONE_NUMBER")

# ----------- Weather API setup -------------
# Values to set with you own credentials/data (env or set directly into the code)
weather_api_key = os.environ.get("OWM_API_KEY")
# -------------------------------------------

client = Client(account_sid, auth_token)
parameters = {
    # Location
    "lat": 0.0,
    "lon": 0.0,
    # Read API : exclude unused info to optimize processing time
    "exclude": "current,minutely,daily",
    "appid": weather_api_key
}

# Request to OWM API (v3.0 version has 401 status : ➡️ using v2.5 until fixed)
response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()

# Slice/Parse to get id value from next 12 hours ('id' corresponds to a code of weather condition)
weather_data = response.json()
hourly_data = weather_data["hourly"][:12]
weather_ids = []
for hour in hourly_data:
    weather_ids.append(hour["weather"][0]["id"])

# Read API doc : If any id is < 700 then you can get (rain/mist/snow/...)
res = any(element < 700 for element in weather_ids)

if res:
    # Code can be scheduled everyday on the beginning of your day (eg. Raspberry PI or Python everywhere)
    # Sends sms if needed else nothing.
    message = client.messages.create(body="You'd better bring an ☂️, big man.",
                                     from_=from_phone_number,
                                     to=my_phone_number)
    print(message.status)
