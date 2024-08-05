import requests
from pytest import mark


@mark.api_test
def test_GePaymentRes(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    url = f"{url_path}/api/Hedge/GetLockHedgeGrafhData?direction=2&pair=USDILS"
    time_point = []
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    hedge = response.json()
    for item in hedge['timesPoints']:
        time_point.append(item)
    assert len(time_point) == 6
