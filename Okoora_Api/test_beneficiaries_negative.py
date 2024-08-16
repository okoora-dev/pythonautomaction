import json
import time
from collections import Counter
from datetime import datetime, timedelta
from pytest import mark
import requests


@mark.regression
def test_add_beneficiary_negative_test(get_path,get_header_data):
    negative_payload={
        "name":"D",
        "country":'IL',
        "idNumber":"",
        "beneficiaryType":3,
        "country_one_letter":"A",
        "city":"",
        "street":"",
        "houseNumber":"",
        "bankCode":"",
        "birthDate": birthday_calc()
    }

    path = get_path
    headers = get_header_data

    payload = get_payload()
    payload['identity']['name']=negative_payload['name']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()
    assert add_response_data['errors']['Identity.Name'][0] == "The length of 'Identity Name' must be at least 2 characters. You entered 1 characters.",f"failed for payload: {payload}"

    payload = get_payload()
    payload['address']['country']=negative_payload['country']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Identity.HebrewName'][0] == "Identity Hebrew Name must be non empty when Country is set to 'IL'",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    payload['identity']['idNumber']=negative_payload['idNumber']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Identity.IdNumber'][0] == "'Identity Id Number' must not be empty.",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    payload['identity']['beneficiaryType']=negative_payload['beneficiaryType']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Identity.CompanyName'][0] == "'Identity Company Name' must not be empty.",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    payload['address']['country']=negative_payload['country_one_letter']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Address.Country'][0] == "Address Country must be a valid ISO 2-letter country code.",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    payload['address']['city']=negative_payload['city']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Address.City'][0] == "'Address City' must not be empty."
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    payload['address']['street']=negative_payload['street']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Address.Street'][0] == "'Address Street' must not be empty.",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    payload['address']['houseNumber']=negative_payload['houseNumber']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Address.HouseNumber'][0] == "'Address House Number' must not be empty.",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    payload['bankAccountInformation']['bankCode']=negative_payload['bankCode']
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['BankAccountInformation.BankCode'][0] == "'Bank Account Information Bank Code' cannot be empty when IBAN field is not supplied",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_payload()
    birthday = birthday_calc()
    payload['identity']['birthDate']=birthday
    add_response = send_add_beneficiary(path,payload,headers)
    print(add_response.text)
    add_response_data = add_response.json()

    assert add_response_data['errors']['Identity.BirthDate'][0] == "Date is Invalid - Age must be at least 18 years old.",f"failed for payload: {payload}"
    assert add_response.status_code == 400,f"failed for payload: {payload}"

    payload = get_positive_payload()
    beneficiary_id = get_approved_beneficiary()
    response_update = update_beneficiary(path, headers, beneficiary_id, payload)
    assert response_update.status_code == 409
    response_update_data = response_update.json()
    assert response_update_data['detail'] == "Cannot update Beneficiary that is on 'Approved' status"
    print(response_update.text)


def send_add_beneficiary(path,payload,headers):
    url = f"{path}/api/v1/Beneficiary/Add"
    response = requests.post(url, json=payload, headers=headers)
    return response


def birthday_calc():
    date_18_years_and_one_day_ago = datetime.now() - timedelta(days=18 * 365.25 -1)
    return date_18_years_and_one_day_ago.strftime('%Y-%m-%d')


def get_payload():
    path = r"../Okoora_Api"
    with open(f"{path}\Api_data.json","r") as file:
        data = json.load(file)
        payload = data['negative_payload']
        return payload


def update_beneficiary(path,headers,beneficiary_id,payload):
    url = f"{path}/api/v1/Beneficiary/{beneficiary_id}"
    response = requests.put(url, headers=headers,json=payload)
    return response

def get_positive_payload():
    path = r"../Okoora_Api"
    with open(f"{path}\Api_data.json","r") as file:
        data = json.load(file)
        payload_iban = data['payload_with_iban']
        return payload_iban

def get_approved_beneficiary():
    path = r"../Okoora_Api"
    with open(f"{path}\Api_data.json","r") as file:
        data = json.load(file)
        beneficiary_id  = data['approved_beneficiary']
        return beneficiary_id
