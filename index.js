import express from "express";
import { chromium } from "playwright";
import axios from "axios";

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", async (req, res) => {
  const pincode = process.env.PINCODE;
  const webhook = process.env.DISCORD_WEBHOOK_URL;

  if (!webhook || !pincode) {
    res.status(500).send("Environment variables not set!");
    return;
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    await page.goto("https://www.flipkart.com");

    // Your scraping logic here
    const message = `Checked stock for pincode ${pincode}`;

    await axios.post(webhook, { content: message });

    res.send(`Done: ${message}`);
  } catch (err) {
    console.error(err);
    res.status(500).send("Error occurred");
  } finally {
    await browser.close();
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
