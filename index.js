import { chromium } from 'playwright';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const PRODUCT_URL = process.env.PRODUCT_URL;  // Flipkart product link
const PINCODE = process.env.PINCODE;          // Desired pincode
const DISCORD_WEBHOOK = process.env.DISCORD_WEBHOOK; // Discord webhook

(async () => {
  const browser = await chromium.launch({
    headless: true,
  });

  const page = await browser.newPage();
  await page.goto(PRODUCT_URL, { waitUntil: 'networkidle' });

  // Example: set pincode
  await page.click('._2P_LDn'); // Pincode field
  await page.fill('._2P_LDn input', PINCODE);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(2000); // wait for refresh

  // Extract stock status
  let stockStatus;
  try {
    stockStatus = await page.textContent('._16FRp0'); // selector for 'Out of Stock'
  } catch {
    stockStatus = 'In Stock';
  }

  // Send to Discord
  await axios.post(DISCORD_WEBHOOK, {
    content: `🔔 Flipkart stock update: **${stockStatus}** for pincode ${PINCODE}\n${PRODUCT_URL}`
  });

  console.log(`Status: ${stockStatus}`);
  await browser.close();
})();
