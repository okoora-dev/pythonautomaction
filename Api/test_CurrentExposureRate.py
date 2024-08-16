import requests
from pytest import mark


@mark.api_test
def test_CurrentExposureRate(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    url = f"{url_path}/api/Rates/CurrentExposureRate?currency=USD"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    payment = response.json()
    assert payment['USD'] > 0.0
    assert payment['ILS'] > 0.0


