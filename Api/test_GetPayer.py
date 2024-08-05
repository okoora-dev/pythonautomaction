import json

import requests
from pytest import mark


@mark.api_test
def test_GetPayer(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    url = f"{url_path}/api/Receiver/GetPayers"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    payers = response.json()
    # print(json.dumps(payers,indent=2))

    for item in payers:
        assert item['accountId'] == data_test['accountId']
