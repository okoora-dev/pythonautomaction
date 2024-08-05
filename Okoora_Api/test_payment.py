import time

import requests
from pytest import mark


@mark.regression
def test_payments(get_path,get_header_data):
    path = get_path
    headers = get_header_data
    payload = {
        "beneficiaryId": "7ACFB8ED-FBA4-46A4-9354-35554897F98C",
        "amount": 150,
        "currency": "ILS"
    }

    # returned_reason = send_payment_reason(path,headers)
    # print(returned_reason.text)
    # assert returned_reason.status_code == 200

    payment_request_response = send_payment_request(path,headers,payload)
    print(payment_request_response.text)
    payment_response_data = payment_request_response.json()
    requestId = payment_response_data['requestId']
    assert payload['currency'] == payment_response_data['send']['currency'],f"failed for payload: {payload['currency']}"
    assert payload['amount'] == payment_response_data['send']['amount'],f"failed for payload: {payload['amount']}"
    assert payment_request_response.status_code == 200,f"failed for payload: {payload}"

    requote_response = send_requote_payment(path,headers,requestId)
    assert requote_response.status_code == 200,f"failed for payload: {payload}"
    requote_response_data = requote_response.json()
    assert payload['currency'] == requote_response_data['send']['currency'],f"failed for payload: {payload['currency']}"
    assert payload['amount'] == requote_response_data['send']['amount'],f"failed for payload: {payload['amount']}"
    calc_exchangeRate = round(float(payload['amount'])/ float(requote_response_data['charge']['amount']),4)
    assert round(calc_exchangeRate,2) == round(requote_response_data['exchangeRate'],2),f"failed for payload: {payload}"
    complete_response = send_complete_payment(path,headers,requestId)
    assert complete_response.status_code == 200,f"failed for payload: {payload}"


def send_payment_reason(path,headers):
    path = path
    headers = headers
    url = f"{path}/api/v1/Payment/PaymentReasons"

    response = requests.get(url, headers=headers)
    print(response.text)
    return response

def send_payment_request(path,headers,payload):
    path = path
    url = f"{path}/api/v1/Payment/PaymentRequest"

    response = requests.post(url, headers=headers,json=payload)
    return response

def send_requote_payment(path,headers,request_id):
    path = path
    url = f"{path}/api/v1/Payment/Requote/{request_id}"
    response = requests.post(url, headers=headers)
    return response


def send_complete_payment(path,headers,request_id):
    requestId = request_id
    path = path
    url = f"{path}/api/v1/Payment/CompletePaymentRequest/{requestId}"
    response = requests.post(url, headers=headers)
    return response
