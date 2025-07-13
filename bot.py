import os
import time
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from flask import Flask
from threading import Thread

# Load Render env vars
PINCODE = os.getenv("PINCODE")
URL = os.getenv("URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

REFRESH_RATE = 30  # seconds between checks

def check_stock():
    print("Notifier started...")

    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            print("Page preview:")
            print(soup.prettify()[:500])

            # Find delivery status element
            delivery_section = soup.find("div", {"class": "_16FRp0"})

            if delivery_section:
                status = delivery_section.get_text(strip=True)
                print(f"Availability status: {status}")

                if "Not deliverable" in status or "Out of Stock" in status or "Coming Soon" in status:
                    msg = f"❌ NOT AVAILABLE for PINCODE {PINCODE}\nStatus: {status}\nURL: {URL}"
                else:
                    msg = f"✅ IN STOCK for PINCODE {PINCODE}!\nStatus: {status}\nURL: {URL}"
            else:
                msg = f"⚠️ Could not detect stock status — check selector!\nURL: {URL}"

            # Send update every check
            print("Sending message to Discord...")
            webhook = DiscordWebhook(
                url=WEBHOOK_URL,
                content=msg
            )
            webhook.execute()

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(REFRESH_RATE)

# --- Flask server for keep-alive ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Flipkart Notifier is running and checking stock for PINCODE " + PINCODE

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- Run both threads ---
if __name__ == "__main__":
    t1 = Thread(target=run_flask)
    t2 = Thread(target=check_stock)

    t1.start()
    t2.start()