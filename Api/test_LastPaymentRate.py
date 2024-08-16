import requests
from pytest import mark


@mark.api_test
def test_LastPaymentRate(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    url = f"{url_path}/api/Rates/LastPaymentRate?currency=USD"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    payment = response.json()
    assert payment['previousPaymentRate'] > 0.0
    assert payment['currentPaymentRate'] > 0.0
    assert payment['percentages'] > 0.0
    assert payment['direction'] > 0.0
    assert payment['buySell'] > 0.0

    print(payment)
