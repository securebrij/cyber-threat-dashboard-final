from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

OTX_API_KEY = os.getenv("OTX_API_KEY")

# Fetch and flatten threat data from AlienVault OTX
def fetch_data_from_otx():
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"  # Use /latest if needed
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        raw_data = res.json().get("results", [])
        return raw_data
    except Exception as e:
        print(f"Error fetching OTX data: {e}")
        return []

# Flatten pulse data into individual threat entries
@app.route("/api/threats")
def get_threats():
    pulses = fetch_data_from_otx()
    threats = []

    for pulse in pulses:
        publisher = pulse.get("author_name", "Unknown")
        title = pulse.get("name", "Unknown Threat")
        created = pulse.get("created", "")
        severity = "Medium"  # Default or customize by pulse tags later

        for ind in pulse.get("indicators", []):
            threats.append({
                "title": title,
                "indicator": ind.get("indicator", "N/A"),
                "type": ind.get("type", "N/A"),
                "publisher": publisher,
                "created": created,
                "severity": severity
            })

    return jsonify(threats)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
