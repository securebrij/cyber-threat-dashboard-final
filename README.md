# 🛡️ Cyber Threat Intelligence Dashboard

A dynamic, interactive dashboard that visualizes real-time cyber threat intelligence data from the AlienVault OTX API. Designed for analysts, students, and security enthusiasts to track global threat activity and gain actionable insights.

![Dashboard Screenshot](static/dashboard.png)

---

## 🌐 Live Demo
🔗 [View Live Dashboard](https://cyber-threat-dashboard.onrender.com)

> Note: This free instance may take a few seconds to wake up due to Render's spin-down behavior.

---

## 🚀 Features

- 🌍 **Interactive Map** – Geolocates and displays threat sources on a dark-themed global map.
- 📊 **Real-Time Threat Feed** – Pulls from AlienVault’s OTX API with current threat indicators.
- 🛠️ **Threat Type Filtering** – Dynamically filter threats by categories (e.g., Malware, Phishing).
- 🎯 **Severity Markers** – Color-coded markers represent severity: High (red), Medium (orange), Low (green).
- 🧩 **Threat Detail Cards** – Hover or click for detailed info including IP, location, and description.
- 🔁 **Auto-Refresh** – Live dashboard refreshes automatically every few minutes.

---

## 🏗️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **Mapping**: Leaflet.js + OpenStreetMap
- **Geolocation API**: IP-API.com
- **Threat Intelligence API**: AlienVault OTX

---

## 📸 Screenshots

| Dashboard Map | Threat Cards |
|---------------|--------------|
| ![Map](static/dashboard.png) | ![Cards](static/dashboard.png) |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cyber-threat-dashboard.git
cd cyber-threat-dashboard
