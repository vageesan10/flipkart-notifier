import express from 'express';
import playwright from 'playwright';
import fetch from 'node-fetch';

const app = express();
const PORT = process.env.PORT || 3000;

const PRODUCT_URL = process.env.PRODUCT_URL;
const PINCODE = process.env.PINCODE;
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

app.get('/', (req, res) => {
  res.send('✅ Flipkart Stock Notifier is running.');
});

app.get('/check', async (req, res) => {
  try {
    const browser = await playwright.chromium.launch();
    const page = await browser.newPage();
    await page.goto(PRODUCT_URL);

    // Example: check stock status
    const availability = await page.textContent('body'); // Replace with actual selector
    console.log(`Availability text: ${availability}`);

    if (availability.includes('In stock')) {
      await fetch(DISCORD_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: `✅ Product is **IN STOCK**!\n${PRODUCT_URL}`,
        }),
      });
    } else {
      console.log('❌ Product not in stock.');
    }

    await browser.close();
    res.send('✅ Stock check done.');
  } catch (err) {
    console.error(err);
    res.status(500).send('❌ Error during check.');
  }
});

// Optional: run check automatically every 5 minutes
setInterval(async () => {
  try {
    const browser = await playwright.chromium.launch();
    const page = await browser.newPage();
    await page.goto(PRODUCT_URL);

    const availability = await page.textContent('body'); // Replace selector
    console.log(`Auto-check: ${availability}`);

    if (availability.includes('In stock')) {
      await fetch(DISCORD_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: `✅ [AUTO] Product is IN STOCK!\n${PRODUCT_URL}`,
        }),
      });
    }

    await browser.close();
  } catch (err) {
    console.error('❌ Error in auto-check:', err);
  }
}, 5 * 60 * 1000); // every 5 mins

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
