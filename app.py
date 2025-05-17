from flask import Flask, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/threats')
def get_threats():
    headers = {"X-OTX-API-KEY": os.environ.get("OTX_API_KEY")}
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json().get("results", [])
    except Exception as e:
        print(f"⚠️ Error fetching from OTX: {e}")
        data = []

    ipv4_threats = []
    for pulse in data:
        for ind in pulse.get("indicators", []):
            if ind.get("type") == "IPv4":
                threat = {
                    "title": pulse.get("name", "Unnamed Threat"),
                    "indicator": ind.get("indicator", "N/A"),
                    "type": ind.get("type", "N/A"),
                    "publisher": pulse.get("author_name", "Unknown"),
                    "severity": classify_severity(pulse.get("name", ""))
                }
                ipv4_threats.append(threat)

    if not ipv4_threats:
        print("⚠️ No valid IPv4 threats found. Using mock fallback.")
        ipv4_threats = [
            {
                "title": "Mock CVE-2025-1234",
                "indicator": "192.168.1.1",
                "type": "Malware",
                "publisher": "AlienVault",
                "severity": "Medium"
            }
        ]

    return jsonify(ipv4_threats)

def classify_severity(title):
    title = title.lower()
    if "zero-day" in title or "exploit" in title:
        return "High"
    elif "phishing" in title or "domain" in title:
        return "Medium"
    else:
        return "Low"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
