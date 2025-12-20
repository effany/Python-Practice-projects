import requests

agify_url = "https://api.agify.io/"
genderize_url = "https://api.genderize.io/"
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

response = requests.get(f"{genderize_url}?name=effany", headers=headers)
data = response.json()
print(data)

blog = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
print(blog.json())