import requests

sample = {"features": [5.1, 3.5, 1.4, 0.2]}
resp = requests.post("http://127.0.0.1:8000/predict", json=sample)
print(resp.json())
