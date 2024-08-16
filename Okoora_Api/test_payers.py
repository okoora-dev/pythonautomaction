import json

import requests
from pytest import mark


@mark.regression
def test_payers(get_path,get_header_data):

    path = get_path
    headers = get_header_data
    payload = {
        "name": "Test",
        "email": "fafjngh@fghg.com",
        "payerType": 2,
        "country": "IL",
        "bankAccountInformation": {
            "iban": "IL280118050000239362314",
            "currency": "ILS"
        },
        "paymentReason": 2
    }
    response_all_payers = get_all_payers(path,headers)
    assert response_all_payers.status_code == 200
    # response_data = response_all_payers.json()
    # print(json.dumps(response_data,indent=2))

    response_add_payer = add_payer(path,headers,payload)
    data_response = response_add_payer.json()
    payer_id = data_response['id']
    assert response_add_payer.status_code == 201

    """Get payer Scenario"""

    response_get_by_id = get_payer_by_id(path,headers,payer_id)
    # print(response_get_by_id.text)
    data_response = response_get_by_id.json()
    # print(data_response)
    assert data_response['id'] == payer_id,f"failed for payload: {payload['id']}"
    assert data_response['email'] == payload['email'],f"failed for payload: {payload['email']}"
    assert data_response['name'] == payload['name'],f"failed for payload: {payload['name']}"
    assert data_response['type'] == payload['payerType'],f"failed for payload: {payload['type']}"
    assert data_response['country'] == payload['country'],f"failed for payload: {payload['country']}"
    assert data_response['iban'] == payload['bankAccountInformation']['iban'],f"failed for payload: {payload['bankAccountInformation']['iban']}"
    assert data_response['paymentReason'] == payload['paymentReason'],f"failed for payload: {payload['paymentReason']}"

    """Update payer scenario"""

    new_payload = get_payload()
    response_update_payer = update_payer(path,headers,new_payload,payer_id)
    assert response_update_payer.status_code == 200,f"failed for payload: {new_payload}"
    response_update_payer_data = response_update_payer.json()
    print(response_update_payer_data)
    assert response_update_payer_data['id'] == payer_id,f"failed for payload: {response_update_payer_data['id']}"
    assert response_update_payer_data['email'] == new_payload['email'],f"failed for payload: {response_update_payer_data['email']}"
    assert response_update_payer_data['name'] == new_payload['name'],f"failed for payload: {response_update_payer_data['name']}"
    assert response_update_payer_data['type'] == new_payload['payerType'],f"failed for payload: {response_update_payer_data['type']}"
    assert response_update_payer_data['country'] == new_payload['country'],f"failed for payload: {response_update_payer_data['country']}"
    assert response_update_payer_data['iban'] == new_payload['bankAccountInformation']['iban'],f"failed for payload: {response_update_payer_data['bankAccountInformation']['iban']}"
    assert response_update_payer_data['paymentReason'] == new_payload['paymentReason'],f"failed for payload: {response_update_payer_data['paymentReason']}"
    assert response_update_payer_data['swiftCode'] == "IDBLILITXXX"

    response_get_by_id = get_payer_by_id(path,headers,payer_id)
    # print(response_get_by_id.text)
    assert response_get_by_id.status_code == 200
    data_response = response_get_by_id.json()
    assert data_response['id'] == payer_id,f"failed for payload: {response_update_payer_data['id']}"
    assert data_response['email'] == new_payload['email'],f"failed for payload: {new_payload['email']}"
    assert data_response['name'] == new_payload['name'],f"failed for payload: {new_payload['name']}"
    assert data_response['type'] == new_payload['payerType'],f"failed for payload: {new_payload['payerType']}"
    assert data_response['country'] == new_payload['country'],f"failed for payload: {new_payload['country']}"
    assert data_response['iban'] == new_payload['bankAccountInformation']['iban'],f"failed for payload: {new_payload['bankAccountInformation']['iban'],}"
    assert data_response['paymentReason'] == new_payload['paymentReason'],f"failed for payload: {new_payload['paymentReason']}"
    assert data_response['swiftCode'] == "IDBLILITXXX"
    response = delete_payer(path,headers,payer_id)
    assert response.status_code == 204,f"failed for payload: {response.text}"


def get_all_payers(path,headers):
    url = f"{path}/api/v1/Payer/All"
    response = requests.get(url, headers=headers)
    print(response.text)
    return response


def add_payer(path,headers,payload):
    url = f"{path}/api/v1/Payer/Add"
    response = requests.post(url, headers=headers,json=payload)
    return response


def delete_payer(path,headers,payer_id):
    url = f"{path}/api/v1/Payer/{payer_id}"
    response = requests.delete(url, headers=headers)
    return response


def get_payer_by_id(path,headers,payer_id):
    url = f"{path}/api/v1/Payer/{payer_id}"
    response = requests.get(url, headers=headers)
    return response


def update_payer(path,headers,payload,payer_id):
    url = f"{path}/api/v1/Payer/{payer_id}"
    result = requests.put(url,headers=headers,json=payload)
    return result


def get_payload():
    with open(r"../Okoora_Api/Api_data.json","r") as file:
        data = json.load(file)
        updated_payload = data['update_payer_payload']
        return updated_payload

