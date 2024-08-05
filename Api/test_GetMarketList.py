import requests
from pytest import mark


@mark.api_test
def test_GetMarketList(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    pair = "USDILS"
    url = f"{url_path}/api/Dashboard/GetMarketListData?pair={pair}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    assert response.status_code == 200
    market = response.json()
    assert market == 4
