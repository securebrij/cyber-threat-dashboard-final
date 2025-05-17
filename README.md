
# 🛡️ Cyber Threat Intelligence Dashboard

A real-time, interactive dashboard that visualizes IPv4-based cyber threats using data from AlienVault OTX. Designed for analysts, students, and security enthusiasts to track global threat activity and gain actionable insights.

![Screenshot](./screenshot.png)

---

## 🚀 Features

- 🌍 **Interactive Map** – Displays threats on a dark-themed global map
- ⚡ **Real-Time Threat Feed** – Pulled directly from AlienVault OTX
- 🔍 **Threat Type Filtering** – Dynamic filtering by threat category
- 🟢 **Severity Tags** – High (Red), Medium (Orange), Low (Green)
- 📋 **Threat Detail Cards** – View details by source, IP, and publisher
- 🔁 **Auto-Refresh** – Dashboard updates automatically every 60 seconds
- 📈 **Analytics** – Bar, Pie, and Timeline charts powered by Chart.js
- 📄 **Export** – Download threat data as CSV
- 🧪 **Mock Fallback** – When API fails, mock threats load automatically
- 🌙 **Dark/Light Mode** – Toggle themes with synced map styling
- 📱 **Responsive UI** – Looks great on desktop or mobile

---

## 🛠️ Tech Stack

**Frontend:**
- HTML, CSS, JavaScript
- Chart.js for analytics
- Bootstrap styling (optional)

**Backend:**
- Python + Flask

**APIs:**
- AlienVault OTX for threat intelligence
- IP geolocation via IP-API (mock-based)

**Mapping:**
- Leaflet.js + OpenStreetMap + Carto Dark Tiles (via Folium or static)

---

## 📸 Screenshots

| Dashboard Map | Threat Cards |
|---------------|--------------|
| ![](./screenshot1.png) | ![](./screenshot2.png) |

---

## 📦 Installation

1. Clone this repo:
```bash
git clone https://github.com/securebrij/cyber-threat-dashboard.git
cd cyber-threat-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OTX API Key:
```bash
export OTX_API_KEY=your_key_here  # For Windows use: set OTX_API_KEY=your_key_here
```

4. Run the app:
```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 📄 License
MIT License © 2025 Brij Patel

## 👤 Author
**Brij Patel**  
📎 [LinkedIn](https://www.linkedin.com/in/brij-patel-6b2a77284)  
💻 [GitHub](https://github.com/securebrij)

---

## 🌐 Live Demo
> Coming soon on [Render](https://render.com)

