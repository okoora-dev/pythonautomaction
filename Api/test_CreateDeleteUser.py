import time

import requests
from pytest import mark

@mark.api_test
def test_CreateDeleteNewUser(data_test):
    url_path = data_test["qa_path"]
    url = f"{url_path}/api/Signup/CreateNewUser"
    payload = {

            "accountType": 2,
            "email": "dapeyos143@usoplay2.com",
            "countryCode": "IL",
            "phoneCode": "972",
            "phoneNumber": "534040500",
            "passwords":
                {
                    "password": "Okoora1!",
                    "confirmPassword": "Okoora1!"
                },
            "role": 1,
            "firstName": "Pay",
            "lastName": "MeRoy",
            "idNumber": "302146871",
            "birthDate": "10-02-1995",
            "city": "Givatayim",
            "address": "blkabka",
            "houseNumber": "234",
            "zipCode": "1242341"
        }

    response = requests.post(url, json=payload)
    assert response.status_code == 200

    profileId = response.json()
    print(profileId)
    time.sleep(1)

    url = f"{url_path}/api/Signup/DeleteAutoAccount?profileId={profileId}"

    response = requests.post(url)
    assert response.status_code == 200






