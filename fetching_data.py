# This program fetches country and continent data and saves them to json files

import json
import requests

country_url = "https://parseapi.back4app.com/classes/Country?count=1&limit=250&excludeKeys=code,phone,native,shape"
continent_url = 'https://parseapi.back4app.com/classes/Continent?count=1&limit=10'
headers = {
    'X-Parse-Application-Id': 'mxsebv4KoWIGkRntXwyzg6c6DhKWQuit8Ry9sHja',
    'X-Parse-Master-Key': 'TpO0j3lG2PmEVMXlKYQACoOXKQrL3lwM0HwR9dbH'
}
country_data = json.loads(requests.get(country_url, headers=headers).content.decode('utf-8'))
country_json_data = json.dumps(country_data, indent=2)
with open("country_data.json", "w") as fname1:
    fname1.write(country_json_data)


continent_data = json.loads(requests.get(continent_url, headers=headers).content.decode('utf-8'))
continent_json_data = (json.dumps(continent_data, indent=2))
with open("continent_data.json", "w") as fname2:
    fname2.write(continent_json_data)

