from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running!"

@app.route("/scrape")
def scrape():
    url = "https://example.com"  # 👈 Replace with your target page
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Example: get page title
    page_title = soup.title.string if soup.title else "No title"

    return jsonify({
        "url": url,
        "title": page_title
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)