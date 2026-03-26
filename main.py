import os
import smtplib
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Tuple

import requests
from dotenv import load_dotenv


def fetch_rain(latitude: float, longitude: float) -> Tuple[float, float]:
    today = date.today()
    tomorrow = today + timedelta(days=1)

    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=rain_sum&timezone=auto&start_date={today}&end_date={tomorrow}"
    )

    return response.json()["daily"]["rain_sum"]


if __name__ == "__main__":
    load_dotenv()

    mail = os.environ["MAIL"]

    latitude = float(os.environ["LATITUDE"])
    longitude = float(os.environ["LONGITUDE"])

    rain_sum_threshold = float(os.environ["RAIN_SUM_THRESHOLD"])

    # fetch predicted rain data
    rain_sum_today, rain_sum_tomorrow = fetch_rain(latitude, longitude)

    # fill values
    if rain_sum_today <= rain_sum_threshold and rain_sum_tomorrow <= rain_sum_threshold:
        central_message = (
            "BEWÄSSERN<br />Es sieht trocken aus. Die Wiese könnte Durst haben."
        )
        central_message_color = "red"
    else:
        central_message = "ENTSPANNEN<br />Es sieht nass aus. Lass die Natur walten."
        central_message_color = "green"

    bg_red = "#aa2200"
    bg_green = "#009922"

    if rain_sum_today <= rain_sum_threshold:
        rain_sum_today_color = bg_red
        rain_sum_today_emoji = "🔴"
    else:
        rain_sum_today_color = bg_green
        rain_sum_today_emoji = "🟢"

    if rain_sum_tomorrow <= rain_sum_threshold:
        rain_sum_tomorrow_color = bg_red
        rain_sum_tomorrow_emoji = "🔴"
    else:
        rain_sum_tomorrow_color = bg_green
        rain_sum_tomorrow_emoji = "🟢"

    # construct mail
    with open("mail_template.html", "r", encoding="utf-8") as file:
        mail_template = file.read()

    mail_content = (
        mail_template.replace("{{central_message}}", central_message)
        .replace("{{central_message_color}}", central_message_color)
        .replace("{{rain_sum_today}}", str(rain_sum_today))
        .replace("{{rain_sum_tomorrow}}", str(rain_sum_tomorrow))
        .replace("{{rain_sum_today_color}}", rain_sum_today_color)
        .replace("{{rain_sum_today_emoji}}", rain_sum_today_emoji)
        .replace("{{rain_sum_tomorrow_color}}", rain_sum_tomorrow_color)
        .replace("{{rain_sum_tomorrow_emoji}}", rain_sum_tomorrow_emoji)
    )

    msg = MIMEMultipart()
    msg["From"] = mail
    msg["To"] = mail
    msg["Subject"] = f"Dein Wiesenwatch: {central_message.split('<br />')[0]}"
    msg.attach(MIMEText(mail_content, "html"))

    # send mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login(mail, os.environ["KEY"])
    server.sendmail(
        mail,
        mail,
        msg.as_string(),
    )
    server.quit()
