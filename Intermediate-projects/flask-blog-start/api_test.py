import requests

url = "https://api.npoint.io/c790b4d5cab58020d391"
data = requests.get(url).json()

print(data)