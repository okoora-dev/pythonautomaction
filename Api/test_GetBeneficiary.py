import json

import requests
from pytest import mark


@mark.api_test
def test_Getbeneficiaries(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    beneficiaryId = data_test["beneficiaryId"]
    url = f"{url_path}/api/Beneficiary/Get?id={beneficiaryId}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    assert response.status_code == 200
    # beneficiaries = response.json()
    # print(json.dumps(beneficiaries,indent=2))
