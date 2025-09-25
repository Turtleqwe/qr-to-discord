import os
import requests
from flask import Flask, request

app = Flask(__name__)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # set this in Render (do NOT commit)

def send_to_discord(content="Scanned"):
    if not WEBHOOK_URL:
        app.logger.error("WEBHOOK_URL not set")
        return False
    try:
        r = requests.post(WEBHOOK_URL, json={"content": content}, timeout=5)
        r.raise_for_status()
        return True
    except Exception as e:
        app.logger.exception("Failed to send webhook")
        return False

@app.route("/", methods=["GET"])
def scanned():
    # minimal message; you can add more info (request.remote_addr, query params, etc.)
    send_to_discord("Scanned")
    return "✅ Thanks for scanning!"
