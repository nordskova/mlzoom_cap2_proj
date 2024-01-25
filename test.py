import requests

url = 'http://localhost:9696/predict'
data = {"img url": " "}


result = requests.post(url, json=data).json()
print(result)