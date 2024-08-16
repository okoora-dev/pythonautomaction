import json

import requests
from pytest import mark


@mark.api_test
def test_CreateFuturePayment(manager_data_test, get_tomorrow_date):
    authorization = manager_data_test['Autho']
    url_path = manager_data_test["demo_path"]
    date = get_tomorrow_date
    print(date)

    url = f"{url_path}/api/Hedge/CreateHedgeByCategory?amount=100000&productType=2&expiryDate={date}&currencyPair=USDILS&direction=2"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.post(url, headers=headers)
    assert response.status_code == 200

    result = response.json()
    print(result)
    url = f"{url_path}/api/Hedge/CompleteQuickHedge?StrategyId={result['strategyId']}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.post(url, headers=headers)
    assert response.status_code == 403
    assert response.reason == "Forbidden"





