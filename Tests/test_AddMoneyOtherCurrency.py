import json
import time

import pytest
import requests

@pytest.mark.qa
@pytest.mark.regression
def test_send_payment(sql_query):
    status = sql_query.delete_from_webhookoutlogs("2414")
    assert "Deleted" in status
    url = "https://okoora-qa-api2023.azurewebsites.net/api/Authentication/login"
    payload = {
        "password": "Okoora2!",
        "username":"jipop81748@in2reach.com"
    }
    headers = {
        "content-type": "application/json"
    }
    response = requests.post(url,json=payload,headers=headers)
    print(response.reason)
    response_data = response.json()
    accessToken = response_data['accessToken']
    print(accessToken)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }
    url ="https://okoora-qa-api2023.azurewebsites.net/api/Cloud/FundingCreate?sender_name= jipop81748@in2reach.com&sender_country=GB&sender_reference=sender-ref&sender_account_number=0050000322&sender_routing_code=&receiver_account_number=GB93TCCL12345622577524&amount=2000&currency=USD"
    payment_response = requests.post(url,headers=headers)
    print(payment_response.status_code)
    time.sleep(5)
    raw_num = sql_query.get_from_webhookoutlogs("2414")
    assert raw_num == 2414

