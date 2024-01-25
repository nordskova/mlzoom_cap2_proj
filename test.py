import requests

url = 'http://localhost:9696/predict'
data = {"img url": "https://raw.githubusercontent.com/nordskova/mlzoom_cap2_proj/main/peng_img.jpeg"}


result = requests.post(url, json=data).json()
print(result)