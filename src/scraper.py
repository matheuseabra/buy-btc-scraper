import requests
import os
import smtplib
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


URL_TO_SCRAP = os.environ.get("URL_TO_SCRAP")
    
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.97 Chrome/78.0.3904.97 Safari/537.36"
}


def check_price(buy_price):
    page = requests.get(URL_TO_SCRAP, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    btc_price = soup.find(href="/currencies/bitcoin/#markets").get_text()

    converted = float(btc_price[1:5])

    print(f"Current price: ${converted}")

    if converted < buy_price:
        send_mail(os.environ["EMAIL_TO"], os.environ["EMAIL_FROM"])


def send_mail(to, fr):
    server = smtplib.SMTP(os.environ["SMTP_HOST"], os.environ["SMTP_PORT"])
    server.ehlo()
    server.starttls()
    server.ehlo()

    sender = "Sender <from@smtp.mailtrap.io>"
    receiver = "Receiver <to@smtp.mailtrap.io>"

    subject = "BTC price fell down"
    body = (
        "Current BTC price is below your buy price. Check out https://coinmarketcap.com"
    )
    msg = f"Subject: {subject}\n\n {body}"

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_PASSWORD"])
        server.sendmail(sender, receiver, msg)
        print("Email has been sent")


while True:
    check_price(8600)
    time.sleep(60)
