import requests

url = "http://127.0.0.1:8000/api/users/login/"
data = {"username": "testuser", "password": "123456"}

response = requests.post(url, json=data)

# 打印登录返回的 Token
print(response.json())
