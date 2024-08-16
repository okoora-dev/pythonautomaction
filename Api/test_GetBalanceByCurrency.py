import requests
from pytest import mark


@mark.api_test
def test_GeBalanceByCurruncy(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    url = f"{url_path}/api/Balances/GetBalancesByCurrency?currency=USD"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    wallet = response.json()
    assert wallet['wallet_Currency']['code'] == "USD"
    assert wallet['wallet_Amount'] > 0.0
