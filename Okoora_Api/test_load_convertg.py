import requests


def test_load_convert():
    for _ in range(20):
        path = "https://okoora-web-api-stage.azurewebsites.net"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Api-Key":  "Okoora_AjbqC94yqGVSujVDRLY3Z5lXpVKXNFbq",
            "X-Client-Id": "b595f697-14fc-4ba7-9091-039254bd41f8"
        }

        payload = {
            "buy": {
                "currency": "USD",
                "amount": 400
            },
            "charge": {
                "currency": "ILS",
                 "amount": None
            }
        }

        send_convert_request(path,headers,payload)


def send_convert_request(path,headers,payload):
    url= f"{path}/api/v1/Convert/ConvertRequest"
    response =requests.post(url, json=payload, headers=headers)
    print(f"status:  {response.status_code} Reason {response.reason}")
