import itertools
import requests
from pytest import mark


@mark.regression
def test_payments_negative(get_path,get_header_data):
    path = get_path
    headers = get_header_data
    payload = {
        "beneficiaryId": "7ACFB8ED-FBA4-46A4-9354-35554897F98C",
        "amount": "",
        "currency": "ILS"
    }
    items = get_payload_options()
    for item in items:
        payload['amount']=item[0]
        # payload['currency'] = item[0]
        payment_request_response = send_payment_request(path,headers,payload)
        assert payment_request_response.status_code == 400,f"failed for payload: {payload}"
def send_payment_request(path,headers,payload):
    path = path
    url = f"{path}/api/v1/Payment/PaymentRequest"

    response = requests.post(url, headers=headers,json=payload)
    return response

def get_payload_options():
    options = [-100,0,""]
    matrix = [list(pair) for pair in itertools.product(options, repeat=1)]
    for item in matrix:
        yield item