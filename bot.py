import os
import time
from discord_webhook import DiscordWebhook
from flask import Flask
from threading import Thread

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
URL = os.getenv("URL")

REFRESH_RATE = 10  # seconds
MESSAGE_COUNT = 5  # send 5 test messages

def check_stock():
    print("Notifier started...")
    sent_count = 0
    while sent_count < MESSAGE_COUNT:
        try:
            webhook = DiscordWebhook(
                url=WEBHOOK_URL,
                content=f"✅ TEST: This is test message {sent_count + 1}! URL: {URL}"
            )
            webhook.execute()
            print(f"Sent test message {sent_count + 1}")
            sent_count += 1
        except Exception as e:
            print(f"Error sending: {e}")
        time.sleep(REFRESH_RATE)

# --- Flask server to keep alive ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Flipkart Notifier is running (TEST MODE)!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- Start both threads ---
if __name__ == "__main__":
    t1 = Thread(target=run_flask)
    t2 = Thread(target=check_stock)

    t1.start()
    t2.start()