import requests
from requests import request
import settings
from client import oauth

# types = ["Part", "Owner", "Project", "Consumable", "Budget", "Assembly", "Machine", "Worker", "Organization",
#          "Expedition"]

types = ["Part", ]
host = "193.136.195.33/ww4"
# host = "localhost:8000"
# url=f"http://{host}/api/v1/consumable/?q=belongsTo==%22urn:ngsi-ld:Project:Chanut%22"
resource = "consumable"
url = f'http://{host}/api/v1/{resource}/?limit=1000&q=belongsToFurniture=="urn:ngsi-ld:Furniture:Porto_group1_subgroup00_Balcaocustomer_wXjG6KMa2eAaL079Porto"'
# url = f'http://{host}/api/v1/{resource}/?limit=1000&q=belongsTo=="urn:ngsi-ld:Project:Chanut"'
data = requests.get(url, auth=oauth,)
parts = data.json()
print(data.status_code, parts)
if data.status_code == 200:
    for part in parts:
        response = requests.delete(url=f"http://{host}/api/v1/{resource}/{part.get('id')}", auth=oauth,)
        print(response.status_code, response.json(), response.url)
