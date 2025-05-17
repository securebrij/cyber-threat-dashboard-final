
import requests
from flask import Flask, jsonify, render_template
import os
import time

app = Flask(__name__)
API_KEY = os.getenv("OTX_API_KEY", "your-api-key")
BASE_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"

def assign_severity(title):
    title = title.lower()
    if any(keyword in title for keyword in ["ransomware", "critical", "exploit", "apt"]):
        return "High"
    elif any(keyword in title for keyword in ["scan", "brute", "suspicious"]):
        return "Low"
    return "Medium"

def mock_data():
    return [
        {
            "indicator": "192.168.1.100",
            "title": "Mock Threat: Ransomware",
            "created": "2025-05-17",
            "publisher": "Mock Publisher",
            "type": "IPv4",
            "severity": "High",
            "location": "Mockville",
            "latitude": 0.0,
            "longitude": 0.0
        },
        {
            "indicator": "10.0.0.45",
            "title": "Mock Threat: Brute Force",
            "created": "2025-05-17",
            "publisher": "Mock Publisher",
            "type": "IPv4",
            "severity": "Low",
            "location": "Mockland",
            "latitude": 0.0,
            "longitude": 0.0
        }
    ]

def fetch_paginated_threats(limit=10, max_pages=1):
    all_indicators = []
    headers = {"X-OTX-API-KEY": API_KEY}
    for page in range(1, max_pages + 1):
        for attempt in range(3):
            try:
                print(f"Fetching page {page}, attempt {attempt + 1}...")
                response = requests.get(f"{BASE_URL}?limit={limit}&page={page}", headers=headers, timeout=10)
                if response.status_code != 200:
                    print(f"Failed on page {page}: {response.status_code}")
                    break
                data = response.json()
                for pulse in data.get("results", []):
                    severity = assign_severity(pulse.get("name", ""))
                    for indicator in pulse.get("indicators", []):
                        if indicator.get("type") == "IPv4":
                            all_indicators.append({
                                "indicator": indicator.get("indicator"),
                                "title": pulse.get("name", "No Title"),
                                "created": pulse.get("created"),
                                "publisher": pulse.get("author_name", "Unknown"),
                                "type": indicator.get("type"),
                                "severity": severity,
                                "location": "Unknown",
                                "latitude": 0.0,
                                "longitude": 0.0
                            })
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)
    if not all_indicators:
        print("No real threats fetched. Injecting mock data...")
        all_indicators = mock_data()
    return all_indicators

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/threats")
def get_threats():
    data = fetch_paginated_threats()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
