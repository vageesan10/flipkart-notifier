import os
import time
from playwright.sync_api import sync_playwright
from discord_webhook import DiscordWebhook

# =============================
# ✅ CONFIG VARIABLES
# =============================

FLIPKART_URL = os.getenv("FLIPKART_URL", "https://www.flipkart.com/your-product-url")
PINCODE = os.getenv("PINCODE", "600001")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # must be set in environment
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))  # seconds

# =============================
# ✅ FUNCTION TO CHECK STOCK
# =============================

def check_stock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(FLIPKART_URL)

        try:
            # Set pincode if needed
            page.click("._2P_LDn")
            page.fill("._36yFo0", PINCODE)
            page.click("._2P_LDn")
            time.sleep(3)
        except Exception as e:
            print(f"Could not set pincode: {e}")

        # Check stock status
        if "Currently out of stock" in page.content() or "Sold Out" in page.content():
            status = "❌ OUT OF STOCK"
        else:
            status = "✅ IN STOCK!"

        print(f"Status: {status}")

        # Send message to Discord
        webhook = DiscordWebhook(
            url=DISCORD_WEBHOOK_URL,
            content=f"{status}\n\n🔗 {FLIPKART_URL}\n📍 Pincode: {PINCODE}"
        )
        webhook.execute()

        browser.close()

# =============================
# ✅ MAIN LOOP
# =============================

if __name__ == "__main__":
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("Missing DISCORD_WEBHOOK_URL in environment!")

    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)