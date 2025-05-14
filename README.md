# HEAD
# 🛡️ Cyber Threat Intelligence Dashboard

A real-time cybersecurity dashboard that pulls the latest threat intel from the [AlienVault OTX](https://otx.alienvault.com/) API. Built using **Flask**, **Python**, and **Jinja2** templates.

## 🌐 Live Preview
Runs locally at `http://127.0.0.1:5000`

## 🚀 Features
- 🔍 Pulls live threat intelligence from OTX
- 🧠 Displays threat names + descriptions
- 📡 Easily extendable with more APIs or visualizations

## 🛠️ Tech Stack
- Python
- Flask
- Requests
- Jinja2
- AlienVault OTX API

## 🧪 How to Run Locally

```bash
git clone https://github.com/brijp1403/cyber-threat-dashboard.git
cd cyber-threat-dashboard
python -m venv venv
.\venv\Scripts\activate
pip install flask requests
python app.py


# 🌐 Cyber Threat Intelligence Dashboard

A real-time, interactive cybersecurity dashboard that visualizes threat intelligence from the AlienVault OTX API. This dashboard includes geolocation mapping, category-based filtering, real-time data refresh, and threat severity overlays.

---

## 🚀 Features

- 🌍 **Interactive Geolocation Map** with threat markers
- 🧠 **Threat Type Filter** to narrow down categories (e.g. Malware, Phishing)
- 🔁 **Real-Time Data Updates** from OTX API
- 🔥 **Color-Coded Severity Indicators**
- 📌 **Marker Clusters & Detail Popups**
- 🎯 **Threat Overlay Cards** with IP, city, and type
- 📱 **Responsive Design** (desktop & mobile friendly)

---

## 🖼️ Screenshot

![Cyber Threat Dashboard](static/dashboard.png)


---

## 🧪 Local Setup

```bash
# Clone the repository
git clone https://github.com/brijp1403/cyber-threat-dashboard.git
cd cyber-threat-dashboard

# Create virtual environment and activate
python -m venv venv
venv\Scripts\activate      # For Windows
# source venv/bin/activate   # For macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

---

## 🌐 Deployment (Optional)

You can deploy this using:

- [Render](https://render.com) with Gunicorn
- [Replit](https://replit.com) or [Glitch](https://glitch.com)
- Docker/Heroku (with adjustments)

---

## 📦 Project Structure

```
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── threat_map.html
│   └── dashboard_screenshot.png
└── README.md
```

---

## 🔐 API Key

To use the AlienVault OTX API:

1. Sign up at https://otx.alienvault.com
2. Generate API key from your profile
3. Paste it inside `app.py` under `X-OTX-API-KEY`

---

## 👨‍💻 Author

**Brij Patel**  
[LinkedIn Profile](https://www.linkedin.com/in/brij-patel-6b2a77284)

---

## 📄 License

MIT License
>>>>>>> b5f0b86 (Added dashboard screenshot to README)
