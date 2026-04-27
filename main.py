import requests
import os 
from datetime import datetime
import smtplib

EMAIL = os.envion.get("MY_GMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")
MY_LAT = 21.448250
MY_LNG = 106.198858


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5


parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
    "tzid": "Asia/Ho_Chi_Minh"
}

def is_dark():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    now_hour = datetime.now().hour
    return sunset <= now_hour or now_hour <= sunrise


if is_dark() and is_overhead():
    with (smtplib.SMTP("smtp.gmail.com", port=587) as connection):
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr =E MAIL,
            to_addrs="nguyenduongminh1112006@gmail.com",
            msg="Subject:Look Up!\n\nThe ISS is above you!"
        )
