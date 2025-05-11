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