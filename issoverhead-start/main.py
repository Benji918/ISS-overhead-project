import requests
from datetime import datetime
import smtplib
import time

my_email = 's@gmail.com' #put your email 
pwd = '' # password
MY_LAT = 6.444550  # Your latitude
MY_LONG = 7.490180  # Your longitude


def current_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_latitude <= MY_LONG + 5:
        return True
    else:
        return False


# Your position is within +5 or -5 degrees of the ISS position.


def night_time():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunset)
    print(sunrise)
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if current_position() and night_time():
        # create connection
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_email, password=pwd)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg='Subject:ISS Satellite overhead\n\n Look up the satellite is crossing your region!!!'
            )

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
