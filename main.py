from flask import Flask, request
import requests
import pandas as pd
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

BASE_URL = 'http://localhost:5001'


@app.route('/predict', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':

        jsonRequest = request.data.decode("utf-8")
        data = pd.read_json(jsonRequest)
        res = data.to_json(orient='split')

        headers = {'Content-Type': 'application/json'}
        r = requests.post(f"{BASE_URL}/invocations", data=str(res), headers=headers)

        result_arr = []

        for i in r.json():
            result_arr.append(i['result'])
        return str(result_arr)

    else:
        return 'Content-Type not supported!'


if __name__ == "__main__":
    app.run("0.0.0.0", 7000, threaded=True)
