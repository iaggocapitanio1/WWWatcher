import requests
from requests import request
import settings
from client import oauth

# types = ["Part", "Owner", "Project", "Consumable", "Budget", "Assembly", "Machine", "Worker", "Organization",
#          "Expedition"]

types = ["Part", ]
# host = "193.136.195.25/ww4"
host = "localhost:8000"


data = requests.get(url=f"http://{host}/api/v1/part/?q=belongsTo==%22urn:ngsi-ld:Project:Braga%22", auth=oauth,)
parts = data.json()
print(data.status_code, parts)
if data.status_code == 200:
    for part in parts:
        response = requests.delete(url=f"http://{host}/api/v1/part/{part.get('id')}", auth=oauth,)
        print(response.status_code)
