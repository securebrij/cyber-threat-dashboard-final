from flask import Flask, render_template, request, jsonify
import requests
import folium
import os
from folium.plugins import MarkerCluster

app = Flask(__name__)

# Fetch threat data from OTX
def get_threat_data():
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {
        "X-OTX-API-KEY": "2649b648d64ca33ba373c6fa1e171589b24af420b2a68cc59c5ece1c1cb9fe5b"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"results": []}

# Get geolocation for an IP

def get_ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return {
                "lat": data['lat'],
                "lon": data['lon'],
                "city": data['city'],
                "country": data['country']
            }
    except:
        pass
    return None

# Parse threat data

def extract_ip_locations(pulse_data, threat_type_filter=None):
    locations = []
    for pulse in pulse_data.get("results", []):
        pulse_type = pulse.get("TLP", "Medium")  # default if not given
        if threat_type_filter and pulse_type != threat_type_filter:
            continue
        for indicator in pulse.get("indicators", []):
            if indicator.get("type") == "IPv4":
                ip = indicator.get("indicator")
                loc = get_ip_geolocation(ip)
                if loc:
                    locations.append({
                        "ip": ip,
                        "pulse": pulse.get("name", "Unknown Threat"),
                        "lat": loc['lat'],
                        "lon": loc['lon'],
                        "city": loc['city'],
                        "country": loc['country'],
                        "severity": pulse_type
                    })
    return locations

# Generate threat map

def generate_threat_map(locations):
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB dark_matter')
    cluster = MarkerCluster().add_to(m)

    for loc in locations:
        color = {
            "High": "red",
            "Medium": "orange",
            "Low": "green"
        }.get(loc.get("severity", "Medium"), "blue")

        popup = f"<b>{loc['pulse']}</b><br>{loc['city']}, {loc['country']}<br>{loc['ip']}"

        folium.Marker(
            location=[loc["lat"], loc["lon"]],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(cluster)

    map_path = os.path.join("static", "threat_map.html")
    m.save(map_path)
    return map_path

@app.route("/")
def home():
    threat_type = request.args.get("type", "All")
    data = get_threat_data()
    locations = extract_ip_locations(data, None if threat_type == "All" else threat_type)
    map_path = generate_threat_map(locations)
    return render_template("index.html", threat_map=map_path, threats=locations, selected_type=threat_type)

@app.route("/api/threats")
def api_threats():
    data = get_threat_data()
    locations = extract_ip_locations(data)
    return jsonify(locations)

if __name__ == "__main__":
    app.run(debug=True, port=10000, host='0.0.0.0')
