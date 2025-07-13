import os
import time
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from flask import Flask
from threading import Thread

# Load your Render env variables
PINCODE = os.getenv("PINCODE")
URL = os.getenv("URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

REFRESH_RATE = 30  # seconds between checks
MESSAGE_COUNT = 5  # how many times to send

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

            # Check Flipkart's availability element
            availability = soup.find("div", {"class": "_16FRp0"})
            if availability:
                status = availability.get_text(strip=True)
                print(f"Availability status: {status}")

                if "Sold Out" not in status and "Coming Soon" not in status:
                    webhook = DiscordWebhook(
                        url=WEBHOOK_URL,
                        content=f"✅ Product is AVAILABLE! {URL}"
                    )
                    webhook.execute()
                    print(f"Notification sent ({sent_count + 1}/{MESSAGE_COUNT})")
                    sent_count += 1
                else:
                    print("Product still out of stock...")
            else:
                print("Could not find availability status — check selector!")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(REFRESH_RATE)

# --- Flask keep-alive ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Flipkart Notifier is running (REAL MODE)!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- Run both threads ---
if __name__ == "__main__":
    t1 = Thread(target=run_flask)
    t2 = Thread(target=check_stock)

    t1.start()
    t2.start()