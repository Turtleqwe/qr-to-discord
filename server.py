import os
import requests
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Set this in Render

def send_to_discord(scan_id, ip_address):
    if not WEBHOOK_URL:
        app.logger.error("WEBHOOK_URL not set")
        return False

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    embed = {
        "title": "📷 QR Code Scanned!",
        "color": 0x00ff00,  # green
        "fields": [
            {"name": "ID", "value": scan_id, "inline": True},
            {"name": "IP", "value": ip_address, "inline": True},
            {"name": "Time", "value": timestamp, "inline": False},
        ]
    }
    payload = {"embeds": [embed]}

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        r.raise_for_status()
        return True
    except Exception as e:
        app.logger.exception("Failed to send webhook")
        return False

@app.route("/", methods=["GET"])
def scanned():
    scan_id = request.args.get("id", "Unknown")
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    send_to_discord(scan_id, ip_address)
    return f"✅ Thanks for scanning ({scan_id})!"

if __name__ == "__main__":
    # Use Render's PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
