const express = require('express');
const { chromium } = require('playwright');

// Use ESM-style fetch in CommonJS safely
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

const app = express();
const PORT = process.env.PORT || 10000;

// Read ENV variables
const PRODUCT_URL = process.env.PRODUCT_URL;
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

// Check config at startup
if (!PRODUCT_URL) {
  throw new Error('❌ Missing PRODUCT_URL env variable!');
}

if (!DISCORD_WEBHOOK_URL) {
  throw new Error('❌ Missing DISCORD_WEBHOOK_URL env variable!');
}

// Stock check function
async function checkStock() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(PRODUCT_URL, { waitUntil: 'domcontentloaded' });

  const pageContent = await page.content();
  let status = 'OUT OF STOCK';

  if (pageContent.includes('Add to cart') || pageContent.includes('Add to Cart')) {
    status = 'IN STOCK ✅';
  }

  await fetch(DISCORD_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: `Flipkart Stock Status: ${status}` }),
  });

  await browser.close();
  return status;
}

// Keepalive ping
async function keepAlive() {
  await fetch(DISCORD_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: '✅ Flipkart notifier is running (ping every 10s)' }),
  });
}

app.get('/', async (req, res) => {
  const result = await checkStock();
  res.send(`Checked: ${result}`);
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  setInterval(keepAlive, 10_000);
});
