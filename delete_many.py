import requests
from requests import request
from settings.client import oauth
from settings.settings import ORION_HOST, ORION_HEADERS

data = requests.get(url=ORION_HOST+"/ngsi-ld/v1/entities?type=Part", auth=oauth, headers=ORION_HEADERS)

parts = data.json()

for part in parts:
    response = requests.delete(url=ORION_HOST + f"/ngsi-ld/v1/entities/{part.get('id')}", auth=oauth,
                               headers=ORION_HEADERS)
    print(response.status_code)
