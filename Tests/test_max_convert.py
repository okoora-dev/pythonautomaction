import json
import pytest
import requests

@pytest.mark.order(2)
@pytest.mark.max
def test_convert(get_user_data):
    user_data = get_user_data
    amount = user_data['amount']
    currencies = user_data['currency']
    path = user_data['path']
    auth = user_data['Auth']
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth}"
    }
    for currency in currencies:
        convert_response = send_convert_request(path,headers,amount,currency)
        convert_data_response = convert_response.json()
        request_id = convert_data_response['convertRequest']['requestId']
        save_request_id(request_id)
        assert convert_response.status_code == 200
        complete_response = complete_convert(path,headers,request_id)
        print(complete_response.text)
        assert complete_response.status_code


def send_convert_request(path,headers,amount,currency):
    url = f"{path}/api/payment/ConvertRequest?Buy.Amount={amount}&Buy.Currency={currency}&Charge.Currency=ILS"
    response = requests.post(url,headers=headers)
    print(response.text)
    return response


def complete_convert(path,headers,requset_id):
    url = f"{path}/api/Payment/CompleteConvertRequest?RequestId={requset_id}"
    response = requests.post(url,headers=headers)
    return response


def save_request_id(request_id):
    # Open file and save the auth
    with open('user_data.json', 'r') as file:
        data = json.load(file)
        data["request_id"] = request_id
    with open("user_data.json", "w") as json_file:
        json.dump(data, json_file, indent=2)
