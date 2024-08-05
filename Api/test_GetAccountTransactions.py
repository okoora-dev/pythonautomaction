import requests
from pytest import mark

from datetime import datetime


@mark.api_test
def test_GetAccountTrans(data_test, get_six_month_date):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    today = datetime.now()
    six_month = get_six_month_date
    print(today.strftime('%d/%m/%Y'))
    url = f"{url_path}/api/Balances/GetAccountTransactions?currency=&FromDate={six_month}&ToDate={today}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
