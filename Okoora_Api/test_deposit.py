import json
from pytest import mark
import requests


@mark.regression
def test_get_bank_to_deposit(get_path,get_header_data):
    path = get_path
    header = get_header_data
    # current_date = datetime.now().strftime("%Y-%m-%d")
    returned_response = send_to_deposit(path,header)
    assert returned_response.status_code == 200,f"failed for payload: {returned_response.text}"
    respond_data = returned_response.json()
    okooraBankId = respond_data[0]['okooraBankId']
    print(okooraBankId)
    data = returned_response.json()
    data_response = json.dumps(data,indent=2)
    print(data_response)


    payload = {
        "depositTransferType": "4",
        "currency": "USD",
        "amount":100,
        "okooraBankId": 13,
        "beneficiaryId": "2de9ce1d-4ec3-42fb-9eaf-11d56d44a326"
    }

    response = send_report_on_deposit(path,header,payload).json()
    print(json.dumps(response,indent=2))


def send_to_deposit(point,header):
    path = point
    headers = header
    print(headers)
    url = f"{path}/api/v1/Deposit/BankAccounts"
    response = requests.get(url,headers=headers)
    return response


def send_report_on_deposit(path,headers,payload):

    url = f"{path}/api/V1/Deposit/ReportOnDeposit"
    response = requests.post(url,headers=headers,json=payload)
    return response

