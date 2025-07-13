import os
import time
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from flask import Flask
from threading import Thread

# Environment variables from Render
PINCODE = os.getenv("PINCODE")
URL = os.getenv("URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

REFRESH_RATE = 30  # seconds between checks
MESSAGE_COUNT = 5  # how many notifications to send

def check_stock():
    print("Notifier started...")
    sent_count = 0
    while sent_count < MESSAGE_COUNT:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            # TEMP: print first part of page to check for CAPTCHA/blocking
            print("Page preview:")
            print(soup.prettify()[:500])

            # BETTER: check for 'Add to cart' button
            add_to_cart = soup.find("button", string="Add to cart")

            if add_to_cart:
                print(f"✅ Product is IN STOCK!")
                webhook = DiscordWebhook(
                    url=WEBHOOK_URL,
                    content=f"✅ REAL: Product is in stock! {URL}"
                )
                webhook.execute()
                sent_count += 1
                print(f"Notification sent ({sent_count}/{MESSAGE_COUNT})")
            else:
                print("❌ Product NOT in stock!")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(REFRESH_RATE)

# --- Flask server for keep-alive ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Flipkart Notifier is running (REAL MODE — Improved)!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- Run both threads ---
if __name__ == "__main__":
    t1 = Thread(target=run_flask)
    t2 = Thread(target=check_stock)

    t1.start()
    t2.start()