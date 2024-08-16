import random
import time

from pytest import mark
import requests

@mark.regression

def test_register_user(get_path,get_header_data):
    time.sleep(5)
    path = get_path
    headers = get_header_data
    reference_number =  random.randint(10000000, 99999999)
    payload = {
        "fullName": "Daniel Test",
        "amount": 120,
        "currency": "ILS",
        "reference": str(reference_number)
    }

    deposit_response = send_report_on_deposit(path,headers,payload)
    assert deposit_response.status_code == 202
    #
    response_data = send_get_deposit(path,headers)
    return_data = response_data.json()
    assert response_data.status_code == 200,f"failed for payload: {payload}"
    assert return_data['reference'] == '65002157',f"failed for payload: {return_data['reference']}"
    assert return_data['currency'] == 'ILS',f"failed for payload: {return_data['currency']}"
    assert return_data['amount'] == 120.0,f"failed for payload: {return_data['amount']}"


def send_report_on_deposit(path,headers,payload):
    path = path
    url = f"{path}/api/v1/Cooperation/Deposit"
    response = requests.post(url, json=payload, headers=headers)

    return  response


def send_get_deposit(path,headers):
    reference = "65002157"
    path = path
    url = f"{path}/api/v1/Cooperation/DepositStatus/{reference}"
    response = requests.get(url,headers=headers)

    return response
