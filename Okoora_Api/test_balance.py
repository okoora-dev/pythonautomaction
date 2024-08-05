import requests
from pytest import mark


@mark.regression
def test_get_all_balance(get_path,get_header_data):
    path = get_path
    headers = get_header_data
    response_all_balance = send_all_balance(path,headers)
    all_balance_data = response_all_balance.json()
    balance_id = all_balance_data[5]['balanceId']
    assert response_all_balance.status_code == 200,f"failed for response: {response_all_balance.text}"


    balance_response = get_balance_by_id(path,headers,balance_id)
    assert balance_response.status_code == 200
    balance_response_data = balance_response.json()
    total_amount = balance_response_data['totalAmount']
    available_amount = balance_response_data['availableAmount']
    assert balance_response_data["balanceId"] == balance_id
    assert balance_response_data["currency"] == "CHF"


    balance_response = get_balance_by_currency_name(path,headers,balance_response_data["currency"])
    assert balance_response.status_code == 200
    balance_response_by_currency_data = balance_response.json()
    assert balance_response_by_currency_data["balanceId"] == balance_id
    assert balance_response_by_currency_data["currency"] == balance_response_data["currency"]
    assert balance_response_by_currency_data['totalAmount'] == total_amount
    assert balance_response_data['availableAmount'] == available_amount



def send_all_balance(path,headers):
    url = f"{path}/api/v1/Balance/All"
    response = requests.get(url, headers=headers)
    return response

def get_balance_by_id(path,headers,balance_id):
    url = f"{path}/api/v1/Balance/{balance_id}"
    response = requests.get(url, headers=headers)
    return response

def get_balance_by_currency_name(path,headers,currency_name):
    url = f"{path}/api/v1/Balance?currency={currency_name}"
    response = requests.get(url, headers=headers)
    return response
