from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Your OTX and IP-API keys (ensure OTX_API_KEY is set in Render)
OTX_API_KEY = os.environ.get("OTX_API_KEY")

# Load mock data as fallback
import json
with open("mock_data.json", "r") as f:
    mock_data = json.load(f)

def fetch_threat_data():
    headers = {"X-OTX-API-KEY": OTX_API_KEY} if OTX_API_KEY else {}
    try:
        url = "https://otx.alienvault.com/api/v1/pulses/subscribed"  # or latest
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        pulses = res.json().get("results", [])
    except Exception as e:
        print(f"Error fetching real threat data, using fallback: {e}")
        return mock_data

    processed = []
    for pulse in pulses:
        for ind in pulse.get("indicators", []):
            if ind.get("type") == "IPv4":
                ip = ind.get("indicator")
                location_data = {}  # fallback if geolocation fails
                try:
                    geo = requests.get(f"http://ip-api.com/json/{ip}").json()
                    location_data = {
                        "lat": geo.get("lat"),
                        "lon": geo.get("lon"),
                        "city": geo.get("city"),
                        "country": geo.get("country")
                    }
                except:
                    continue

                processed.append({
                    "title": pulse.get("name"),
                    "type": ind.get("type"),
                    "indicator": ind.get("indicator"),
                    "publisher": pulse.get("author_name", "Unknown"),
                    "severity": pulse.get("threat_hunting_techniques", ["Medium"])[0],
                    "created": pulse.get("created"),
                    **location_data
                })
    return processed if processed else mock_data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/threats')
def threats():
    return jsonify(fetch_threat_data())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
