import time
from datetime import datetime
import smtplib

import requests

MY_LAT = 'ENTER YOUR LATITUDE AS A FLOAT'
MY_LONG = 'ENTER YOUR LONGITUDE AS A FLOAT'

MY_EMAIL = 'ENTER YOUR EMAIL HERE'
MY_PASSWORD = 'ENTER YOUR PASSWORD HERE'


def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')

    response.raise_for_status()

    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    # postion within +5 or -5 degrees of iss position
    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LONG - 5 <= longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0,
    }

    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    # if iss is close to current position and its currently dark send a email
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject: Look up, the ISS is in the sky"
        )
