import os
import time
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from flask import Flask
from threading import Thread

# Load from environment
PINCODE = os.getenv("PINCODE")
URL = os.getenv("URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Other config
REFRESH_RATE = 10  # seconds
MESSAGE_COUNT = 3

def check_stock():
    print("Notifier started...")
    sent_count = 0
    while sent_count < MESSAGE_COUNT:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            availability = soup.find("div", {"class": "_16FRp0"}).get_text().strip()
            print(f"Availability status: {availability}")

            if "Sold Out" not in availability and "Coming Soon" not in availability:
                webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"✅ Product is available! {URL}")
                webhook.execute()
                sent_count += 1
                print(f"Notification sent ({sent_count}/{MESSAGE_COUNT})")
            else:
                print("Still out of stock...")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(REFRESH_RATE)

# ---- Flask keep-alive server ----
app = Flask('')

@app.route('/')
def home():
    return "Flipkart Notifier is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# Run Flask + Notifier together
if __name__ == "__main__":
    t1 = Thread(target=run_web)
    t1.start()

    t2 = Thread(target=check_stock)
    t2.start()
