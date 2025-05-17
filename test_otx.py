import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
api_key = os.getenv("OTX_API_KEY")
url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
headers = {"X-OTX-API-KEY": api_key}

try:
    print("🌐 Fetching data...")
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    data = res.json()
    results = data.get("results", [])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"otx_output_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Data saved to {filename} ({len(results)} pulses)")
except Exception as e:
    print(f"❌ Error fetching data: {e}")
