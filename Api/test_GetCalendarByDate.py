import requests
from pytest import mark
from datetime import datetime


@mark.api_test
def test_GetCalendarByDate(data_test, end_the_year):
    authorization = data_test['Autho']
    url_path = data_test["demo_path"]
    today = datetime.now()
    end_year = end_the_year
    formated_date = today.strftime('%d/%m/%Y')
    url = f"{url_path}/api/Dashboard/GetCalendarByDate?fromDate={formated_date}&toDate={end_year}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print(response.text)
