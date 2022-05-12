# %% Extract data from the API
import pandas as pd
from onboard.client import RtemClient
import requests

api_key='ob-p-J29LKCtf-zqhOxy0Xo1yMpepGNajkI6YHburnjwqr0dkamfXDknS5L-CkRPycfZhXLo'

client = RtemClient(api_key)

# %% get data from api

key = {"key": api_key}
response = requests.post("https://api.onboarddata.io/login/api-key", data=key)
response = response.json()

headers = {"Authorization": "Bearer "+ response["access_token"]}

# %% Get the buildings

"""
bdgs = requests.get("https://api.onboarddata.io/buildings", headers=headers).json()
bdgs[0]
"""
# %% Getting data using the functions from Onboard API

buildings = pd.json_normalize(client.get_all_buildings()).to_csv("buildings.csv", index=False)
equipment = pd.json_normalize(client.get_all_equipment()).to_csv("equipment.csv", index=False)
equipment_types = pd.json_normalize(client.get_equipment_types()).to_csv("equipment_types.csv", index=False)
point_types = pd.DataFrame(client.get_all_point_types()).to_csv("point_types.csv", index=False)
tags = pd.json_normalize(client.get_tags()).to_csv("tags.csv", index=False)
points= pd.json_normalize(client.get_all_points()).to_csv("points.csv", index=False)
point_types = pd.DataFrame(client.get_all_point_types()).to_csv("point_types.csv", index=False)
measurement_types = pd.DataFrame(client.get_all_measurements()).to_csv("measurement_types.csv", index=False)

# %%
