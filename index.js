import express from "express";
import { chromium } from "playwright";
import fetch from "node-fetch";

const app = express();
const PORT = process.env.PORT || 10000;

const PRODUCT_URL = process.env.PRODUCT_URL;
const PINCODE = process.env.PINCODE;
const WEBHOOK_URL = process.env.WEBHOOK_URL;

// Function to check stock
async function checkStock() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(PRODUCT_URL, { waitUntil: "domcontentloaded" });

  // Example: Close login popup if present
  try {
    await page.click("._2KpZ6l._2doB4z", { timeout: 3000 });
  } catch {}

  // Set pincode
  try {
    await page.click("._2P_LDn");
    await page.fill("._36yFo0 input", PINCODE);
    await page.click("._2P_LDn ._2KpZ6l");
    await page.waitForTimeout(2000);
  } catch {}

  let isOutOfStock = false;

  try {
    const outOfStockElement = await page.$("._16FRp0");
    if (outOfStockElement) {
      isOutOfStock = true;
    }
  } catch {}

  await browser.close();
  return isOutOfStock;
}

// Webhook heartbeat every 10 seconds
setInterval(async () => {
  await fetch(WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: "🚀 Flipkart Notifier build is LIVE and RUNNING!" }),
  });
  console.log("Sent heartbeat to Discord");
}, 10000);

// Root endpoint to check stock
app.get("/", async (req, res) => {
  const outOfStock = await checkStock();
  if (outOfStock) {
    await fetch(WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: "❌ Product is OUT OF STOCK" }),
    });
    res.send("❌ Product is OUT OF STOCK");
  } else {
    await fetch(WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: "✅ Product is IN STOCK" }),
    });
    res.send("✅ Product is IN STOCK");
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
