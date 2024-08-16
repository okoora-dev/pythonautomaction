import json
import time
from collections import Counter
from pytest import mark
import requests


@mark.regression
@mark.last
def test_get_beneficiary(get_path,get_header_data):

    path = get_path
    headers = get_header_data
    beneficiary_response = send_all_beneficiary(path,headers)
    beneficiary_data = json.loads(beneficiary_response.text)[0]
    beneficiary_id = beneficiary_data['id']
    assert beneficiary_response.status_code == 200
    data_res = list(beneficiary_response.json()[0])
    count = Counter(data_res)
    assert count['id'] == 1

    response = find_beneficiary_by_id(path,headers,beneficiary_id)
    assert response.status_code == 200
    data_res = list(response.json())
    # print(data_res)
    count = Counter(data_res)
    # print(count['id'])
    assert count['id'] == 1
    #
    payload_list = get_payload()
    for data in payload_list:
        if data[0]['identity']['name'] != "payload_bank_and_iban":
            payload = data[0]
            print(payload)
            add_response = send_add_beneficiary(path,payload,headers)
            print(add_response.text)
            assert add_response.status_code == 201
            response_data = add_response.json()
            assert response_data['status'] == 5
            beneficiary_id = response_data['id']
            payload['identity']['email'] = "test@update.com"
            response_update = update_beneficiary(path,headers,beneficiary_id,payload)
            print(response_update.text)
            delete_response = delete_beneficiary(path,headers,beneficiary_id)
            assert delete_response.status_code == 204
            not_found_response = find_deleted_beneficiary(path,headers,beneficiary_id)
            assert 'Beneficiary is not found' == not_found_response.json()['detail']
            assert not_found_response.status_code == 404
        else:
            payload = data[0]
            add_response = send_add_beneficiary(path,payload,headers)
            print(add_response.text)
            assert add_response.status_code == 400,f"failed for payload: {payload}"




def send_all_beneficiary(path,headers):
    url = f"{path}/api/v1/Beneficiary/All"
    response = requests.get(url, headers=headers)
    return response


def find_beneficiary_by_id(path,headers,beneficiary_id):
    url = f"{path}/api/v1/Beneficiary/{beneficiary_id}"
    response = requests.get(url, headers=headers)
    return response


def send_add_beneficiary(path,payload,headers):
    url = f"{path}/api/v1/Beneficiary/Add"
    response = requests.post(url, json=payload, headers=headers)
    return response


def delete_beneficiary(path,headers,beneficiary_id):
    url = f"{path}/api/v1/Beneficiary/{beneficiary_id}"
    response = requests.delete(url, headers=headers)
    return response


def find_deleted_beneficiary(path,headers,beneficiary_id):
    url = f"{path}/api/v1/Beneficiary/{beneficiary_id}"
    response = requests.get(url, headers=headers)
    return response


def update_beneficiary(path,headers,beneficiary_id,payload):
    url = f"{path}/api/v1/Beneficiary/{beneficiary_id}"
    response = requests.put(url, headers=headers,json=payload)
    return response

def get_payload():
    with open(r"../Okoora_Api/Api_data.json","r") as file:
        data = json.load(file)
        payload_iban = data['payload_with_iban']
        payload_with_bank_detail = data['payload_with_bank_detail']
        payload_bank_and_iban = data['payload_bank_and_iban']
        list_of_payload = [payload_iban,payload_with_bank_detail,payload_bank_and_iban]
        yield list_of_payload
