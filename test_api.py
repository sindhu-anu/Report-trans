import requests

url = "http://127.0.0.1:8000/process"

files = {"image": open(r"C:\Sem 4\Report-trans\report1.jpg", "rb")}

res = requests.post(url, files=files)

print(res.json())