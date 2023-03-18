# -*- coding: utf-8 -*-

from datetime import datetime

import requests

localhost = " http://127.0.0.1:8000"

# 1. Upload data to market
payload = [
    dict(timestamp=str(datetime.now()), asset="BRN", price=101),
    dict(timestamp=str(datetime.now()), asset="HH", price=9),
]
response = requests.post(f"{localhost}/market/upload_data/", json=payload)
print(response.status_code)


# 2. Retrieve the latest price for a list of assets
response = requests.get(f"{localhost}/market/get_latest_prices/")
print(response.text)


# 3. Calculate PV of options
payload = [
    "BRN Jan24 Call Strike 100 USD/BBL",
    "HH Mar24 Put Strike 10 USD/MMBTu",
]
response = requests.post(f"{localhost}/options/calculate_pv/", json=payload)
print(response.text)
