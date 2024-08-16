import pytest
import pytest
import requests


@pytest.mark.regression
@pytest.mark.run(order=1)


def test_convert(get_path,get_header_data,buy_currency="USD",buy_amount=400,currency="ILS",amount=None):
    path = get_path
    headers = get_header_data

    payload = {
        "buy": {
            "currency": buy_currency,
            "amount": buy_amount
        },
        "charge": {
            "currency": currency,
             "amount": amount
        }
    }

    convert_response = send_convert_request(path,headers,payload)
    if convert_response.status_code == 200:
        res_data = convert_response.json()
        request_id = res_data['requestId']
        # print(res_data)

        requote_res = send_requote(path,headers,request_id).json()
        requote_res = requote_res
        # json_requote_res = json.dumps(requote_res,indent=2)
        assert requote_res['requestId'] == request_id
        assert requote_res['buy']['currency'] == payload['buy']['currency']
        assert int(requote_res['buy']['amount']) == payload['buy']['amount']
        assert requote_res['charge']['currency'] == payload['charge']['currency']
        assert requote_res['charge']['amount'] == res_data['charge']['amount']
        assert requote_res['exchangeRate'] == res_data['exchangeRate']

        complete_response = send_complete_convert(path,headers,request_id)
        print(complete_response.text)
        assert complete_response.status_code == 200,f"failed for payload: {payload}"


def send_convert_request(path,headers,payload):
    url= f"{path}/api/v1/Convert/ConvertRequest"
    response = requests.post(url, json=payload, headers=headers)
    return response


def send_requote(path,headers,request_id):
    url = f"{path}/api/v1/Convert/Requote/{request_id}"
    response = requests.post(url, headers=headers)
    return response


def send_complete_convert(path,headers,request_id):
    url = f"{path}/api/v1/Convert/CompleteConvertRequest/{request_id}"
    response =requests.post(url, headers=headers)
    return response
