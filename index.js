const express = require('express');
const { chromium } = require('playwright');

const fetch = (...args) =>
  import('node-fetch').then(({ default: fetch }) => fetch(...args));

const app = express();
const PORT = process.env.PORT || 10000;

const PRODUCT_URL = process.env.PRODUCT_URL;
const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;

async function checkStock() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(PRODUCT_URL, { waitUntil: 'domcontentloaded' });

  const pageContent = await page.content();
  let status = 'OUT OF STOCK';

  if (pageContent
