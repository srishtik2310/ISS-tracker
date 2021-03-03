# add your mail and password from which you want to send mail
# change the To address to which you want to send notification
# change MY_LAT(latitude) and MY_LONG(longitude) according to your location

import requests
from datetime import datetime
import smtplib

MY_LAT = 12.904110 # Your latitude
MY_LONG = 75.041367 # Your longitude
TO_ADDRESS = "example@gmail.com"

MY_MAIL = "example2@gmail.com"
PASSWORD = "password"
connection = smtplib.SMTP("smtp.gmail.com", 587)


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5.5
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5.5

time_now = datetime.now().hour

def is_iss_overhead():
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return  False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = (int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5.5)
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5.5

    time_now = datetime.now().hour

    if time_now >= sunset or time_now < sunrise:
        return True
    else:
        return False

def send_mail():
    if is_iss_overhead() and is_night():
        connection.starttls()
        connection.login(user=MY_MAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_MAIL, to_addrs= f"{TO_ADDRESS}",
                            msg=f"Subject:ISS Overhead!!\n\n Hey, ISS is passing over your location.")
        connection.close()

send_mail()