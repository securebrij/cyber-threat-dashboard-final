from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    data = get_threat_data()
    return render_template('index.html', data=data)

def get_threat_data():
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {
        "X-OTX-API-KEY": "2649b648d64ca33ba373c6fa1e171589b24af420b2a68cc59c5ece1c1cb9fe5b"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"results": []}

if __name__ == "__main__":
    app.run(debug=True)

