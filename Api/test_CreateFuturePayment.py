import requests
from pytest import mark


@mark.api_test
def test_CreateFuturePayment(data_test, get_tomorrow_date):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    beneficiaryId = "c52f5054-daa4-4129-bcc6-ed0a33cdde9d"
    date = get_tomorrow_date
    print(date)

    url = f"{url_path}/api/Hedge/CreateFuturePayment?amount=100&currency=ILS&expiryDate={date}&beneficiaryId={beneficiaryId}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.post(url, headers=headers)
    print(response.text)
    assert response.status_code == 200
