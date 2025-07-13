import express from 'express';
import fetch from 'node-fetch';
import playwright from 'playwright';

const app = express();

const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;
const PRODUCT_URL = process.env.PRODUCT_URL;

if (!DISCORD_WEBHOOK_URL) {
  throw new Error('❌ Missing DISCORD_WEBHOOK_URL env variable!');
}

if (!PRODUCT_URL) {
  throw new Error('❌ Missing PRODUCT_URL env variable!');
}

async function checkStock() {
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage();
  await page.goto(PRODUCT_URL, { waitUntil: 'domcontentloaded' });

  const content = await page.content();
  if (content.includes('Sold Out')) {
    console.log('❌ Out of Stock');
  } else {
    console.log('✅ In Stock! Sending to Discord...');
    await fetch(DISCORD_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: `🚨 Flipkart item in stock: ${PRODUCT_URL}` }),
    });
  }

  await browser.close();
}

setInterval(checkStock, 60 * 1000); // every minute

const
