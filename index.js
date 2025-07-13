const express = require('express');
const { chromium } = require('playwright');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 10000;

// Load your ENV variables
const PRODUCT_URL = process.env.PRODUCT_URL;
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

// Core check
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

// Keepalive pinger
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

  // Send keepalive every 10s
  setInterval(keepAlive, 10000);
});
