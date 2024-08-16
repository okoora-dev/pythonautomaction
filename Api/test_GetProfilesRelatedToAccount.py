import requests
from pytest import mark
import json


@mark.api_test
def test_GetProfiles(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]

    url = f"{url_path}/api/Account/GetClientProfile"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    result = response.json()

    with open("data.json", "r") as json_file:
        data = json.load(json_file)
        data[0]['accountId'] = result["accountId"]
        data[0]['activateStatus'] = result["activateStatus"]
        data[0]['kycStatus'] = result["kycStatus"]
