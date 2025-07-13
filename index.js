import { chromium } from 'playwright';
import fetch from 'node-fetch';

const PRODUCT_URL = process.env.PRODUCT_URL;
const PINCODE = process.env.PINCODE;
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

async function checkStock() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(PRODUCT_URL, { waitUntil: 'domcontentloaded' });

  // Enter pincode
  await page.fill('input[placeholder="Enter Delivery Pincode"]', PINCODE);
  await page.click('._2P_LDn');

  // Wait for availability info to appear
  await page.waitForTimeout(3000);

  // Example selector: Update according to Flipkart’s page structure
  const stockStatus = await page.$eval('._16FRp0', el => el.textContent);

  if (!stockStatus.includes('Not available')) {
    console.log('Product is available! Sending Discord notification...');
    await fetch(DISCORD_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        content: `✅ Product is in stock! [Check here](${PRODUCT_URL})`
      }),
    });
  } else {
    console.log('Product is not available.');
  }

  await browser.close();
}

checkStock().catch(console.error);
