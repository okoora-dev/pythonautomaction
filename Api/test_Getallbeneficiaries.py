import requests
from pytest import mark


@mark.api_test
def test_Getallbeneficiaries(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    beneficiary_list = []

    url = f"{url_path}/api/Payment/GetAllBeneficieryByAccount"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    assert response.status_code == 200
    beneficiaries = response.json()
    for i in beneficiaries:
        beneficiary_list.append(i['bankAccountHolderName'])

    assert 'Test USD' in beneficiary_list
