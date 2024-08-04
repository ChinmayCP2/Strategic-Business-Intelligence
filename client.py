import requests
import json

url = "http://localhost:8000/send-json/"
payload = {
    "stateCode": 530,
    "districtCode": 1672
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    print("Response received successfully:")
    print(response.json())
else:
    print(f"Failed to get a valid response. Status code: {response.status_code}")
    print("Response content:", response.content)
