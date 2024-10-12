import requests
import json

json_data = {"locations":[]}
with open("testing/output_usa.txt", "r") as file:
    for line in file:
        end_idx = line.index(':')
        payload = {'key': '7A31A4409EB96A8C6966833F42B5E570', 'ip': line[:end_idx], 'format': 'json'}
        api_result = requests.get('https://api.ip2location.io/', params=payload)
        data = json.loads(api_result.text)

        json_data["locations"].append({"ip":"http://"+line[:-1]+"/cgi-bin/guestimage.html", "lat":data["latitude"], "long":data["longitude"]})


filename = 'dump.json'

with open(filename, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)