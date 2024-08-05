import requests
from pytest import mark


@mark.api_test
def test_AllActiveCurrencies(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]

    url = f"{url_path}/Api/Balances/GetAllActiveCurrencies"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    result = response.json()

    code_list = [item["currency"]["code"] for item in result]

    assert len(code_list) == 21
