import datetime as dt
import smtplib
import time
import requests

POZNAN_LAT = 52.4064
POZNAN_LNG = 16.9252

SMTP_MY_EMAIL_ADDRESS = "dummy_email@gmail.com"  # insert email  here
SMTP_PYTHON_APP_PWD = "dummy_secret"  # insert SMTP app secret here

parameters_sunrise_sunset_API = {
    "lat": POZNAN_LAT,
    "lng": POZNAN_LNG,
    "formatted": 0,
}


# sunrise and sunset API
def is_dark_enough():
    response_sunset_sunrise_api = requests.get("https://api.sunrise-sunset.org/json?", params=parameters_sunrise_sunset_API)
    response_sunset_sunrise_api.raise_for_status()

    data_sun_api = response_sunset_sunrise_api.json()
    today_sunrise = int(data_sun_api["results"]["sunrise"].split("T")[1].split(":")[0])
    today_sunset = int(data_sun_api["results"]["sunset"].split("T")[1].split(":")[0])

    current_hour = dt.datetime.now().hour

    return today_sunrise > current_hour or current_hour > today_sunset


# ISS API
def is_iss_close_enough():
    response_iss_api = requests.get("http://api.open-notify.org/iss-now.json")
    response_iss_api.raise_for_status()
    data_iss_api = response_iss_api.json()

    iss_lat = float(data_iss_api["iss_position"]["latitude"])
    iss_lng = float(data_iss_api["iss_position"]["longitude"])

    is_iss_close_enough_lat = POZNAN_LAT - 5 < iss_lat < POZNAN_LAT + 5
    is_iss_close_enough_lng = POZNAN_LNG - 5 < iss_lng < POZNAN_LNG + 5

    return is_iss_close_enough_lat and is_iss_close_enough_lng


while True:
    time.sleep(60)
    print('loop', dt.datetime.now())

    if is_dark_enough() and is_iss_close_enough():
        print('-- -- -- send email - before')

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=SMTP_MY_EMAIL_ADDRESS, password=SMTP_PYTHON_APP_PWD)
            connection.sendmail(
                from_addr=SMTP_MY_EMAIL_ADDRESS,
                to_addrs=SMTP_MY_EMAIL_ADDRESS,
                msg=f"Subject:ISS overhead!\n\nCheck ISS position. It should be near you"
            )

        print('-- -- -- send email - after')
