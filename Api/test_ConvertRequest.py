import requests
from pytest import mark


@mark.api_test
def test_ConvertRequest(data_test):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]

    url = f"{url_path}/api/Payment/ConvertRequest?Charge.Currency=USD&Buy.Currency=EUR&Buy.Amount=100&Charge.Amount=null"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.post(url, headers=headers)
    result = response.json()
    assert result['status'] == "Create Request Successfully"

    requestId = result['convertRequest']['requestId']

    url = f"{url_path}/api/Payment/CheckWalletBalanceForConvert?RequestId={requestId}"
    response = requests.post(url, headers=headers)
    print(response.json())

    url = f"{url_path}/api/Payment/RefreshConvertRequest?RequestId={requestId}"
    response = requests.post(url, headers=headers)

    assert response.status_code == 200

    url = f"{url_path}/api/Payment/CompleteConvertRequest?RequestId={requestId}"
    response = requests.post(url, headers=headers)
    assert response.status_code == 200
