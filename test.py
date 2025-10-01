import requests
response = requests.get("https://www.opentable.com/location/dallas-restaurants")
print(f"Status: {response.status_code}")
print(f"Length: {len(response.text)}")
