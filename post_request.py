import requests
import json

'''
Run this file after running api.py in a separate terminal window
Send a POST request payload, and prints the response
'''

url = "http://localhost:5000"
data = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

try:
    #Timeout after 5 seconds
    r = requests.post(url, data=json.dumps(data), headers=headers, timeout=5)

    if r.status_code == 200:
        response_data = r.json()
        print("Response:", response_data)
    else:
        print("Error:", r.status_code)
        print("Response:", r.text)

except requests.exceptions.RequestException as e:
    print("Error:", e)