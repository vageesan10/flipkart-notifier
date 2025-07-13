#!/usr/bin/env bash

echo "Installing Python deps..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
python -m playwright install

echo "✅ Build done."
