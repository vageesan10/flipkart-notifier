import os
import time
from discord_webhook import DiscordWebhook
from flask import Flask
from threading import Thread
from playwright.sync_api import sync_playwright

PINCODE = os.getenv("PINCODE")
URL = os.getenv("URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

REFRESH_RATE = 30  # seconds

def check_stock():
    print("Notifier started (Playwright version)...")
    while True:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(URL)

                page.wait_for_timeout(5000)  # wait 5 sec for JS to load

                html = page.content()
                print(html[:500])  # debug

                if "Out of Stock" in html or "Currently unavailable" in html:
                    msg = f"❌ NOT AVAILABLE for PINCODE {PINCODE}\nURL: {URL}"
                else:
                    msg = f"✅ IN STOCK for PINCODE {PINCODE}!\nURL: {URL}"

                print(msg)
                webhook = DiscordWebhook(url=WEBHOOK_URL, content=msg)
                webhook.execute()

                browser.close()

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(REFRESH_RATE)

# --- Flask ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Flipkart Notifier running with Playwright"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t1 = Thread(target=run_flask)
    t2 = Thread(target=check_stock)

    t1.start()
    t2.start()