import requests
from pytest import mark


@mark.api_test
def test_GePaymentRes(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    url = f"{url_path}/api/Payment/PaymentReasons"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    beneficiaries = response.json()
    print(beneficiaries)
