import os
import time
from discord_webhook import DiscordWebhook
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

FLIPKART_URL = os.getenv("FLIPKART_URL")
PINCODE = os.getenv("PINCODE")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

def check_stock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(FLIPKART_URL, timeout=60000)
        page.fill('input._36yFo0', PINCODE)
        page.click('._2P_LDn')
        page.wait_for_timeout(5000)
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        out_of_stock = soup.find_all(string=lambda t: 'out of stock' in t.lower())
        browser.close()
        return not out_of_stock

def send_discord_message(msg):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=msg)
    webhook.execute()

if __name__ == "__main__":
    while True:
        try:
            in_stock = check_stock()
            if in_stock:
                send_discord_message(f"✅ IN STOCK at PINCODE {PINCODE}!\n{FLIPKART_URL}")
            else:
                print("❌ Out of stock. Checking again later...")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(CHECK_INTERVAL)