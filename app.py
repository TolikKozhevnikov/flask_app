from flask import Flask, request
import requests
import datetime
import pandas as pd
from prometheus_flask_exporter import PrometheusMetrics
import json
app = Flask(__name__)

metrics = PrometheusMetrics(app)
all_metrics_base = {}
counter = 0

BASE_URL = 'http://10.12.10.20:5001'
METRICS_SERVER_URL = 'http://10.12.10.20:5001'

@app.route('/predict', methods=['POST'])
def predict():
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
        date = datetime.datetime.now()
        global all_metrics_base, counter
        all_metrics_base[counter] = [{'date',
                                       str(date)}, {'result', str(result_arr)}]
        
        counter += 1
        return str(result_arr)

    else:
        return 'Content-Type not supported!'

@app.route('/all_metrics', methods=['GET'])
def all_metrics():
    global all_metrics_base
    return str(json.dumps(all_metrics_base, default=set_default))


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

if __name__ == "__main__":
    app.run("0.0.0.0", 7000, threaded=True)
