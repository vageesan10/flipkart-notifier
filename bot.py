import os
import time
from discord_webhook import DiscordWebhook
from bs4 import BeautifulSoup
from flask import Flask
from playwright.sync_api import sync_playwright

FLIPKART_URL = os.environ.get("FLIPKART_URL")
PINCODE = os.environ.get("PINCODE")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Playwright Flipkart Notifier is running!"

def check_stock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(FLIPKART_URL, timeout=60000)

        # Click pincode input and enter PIN
        page.click("._36yFo0")   # The pincode input
        page.fill("._36yFo0", PINCODE)
        page.click("._2P_LDn")   # The check button

        # Wait for response to update delivery status
        time.sleep(5)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Flipkart often shows 'Out of Stock' or disables the Buy button
        if soup.find(string=lambda s: "out of stock" in s.lower()):
            status = "❌ OUT OF STOCK"
        else:
            status = "✅ IN STOCK"

        msg = f"{status} at PINCODE `{PINCODE}`\n{FLIPKART_URL}"

        if DISCORD_WEBHOOK_URL:
            DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=msg).execute()

        print(msg)
        browser.close()

if __name__ == "__main__":
    check_stock()
    app.run(host="0.0.0.0", port=8080)
