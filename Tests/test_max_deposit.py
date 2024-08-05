import json
import time

import pytest
import requests

@pytest.mark.order(3)
@pytest.mark.max
def test_max_deposit(get_user_data,sql_query):
    user_data = get_user_data
    request_id = user_data['request_id']
    path = user_data['path']
    auth = user_data['Auth']
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth}"
    }
    deposit_response = send_deposit(path,headers,request_id)
    assert deposit_response.status_code == 201
    sql = sql_query
    row_num = sql.check_row_trans(str(request_id))
    assert row_num == 1
    time.sleep(3)
    sql.approve_deposit(str(request_id))


def send_deposit(path,headers,request_id):
    url = f"{path}/api/balances/DepositRegular?TransferType=2&OkooraBankId=10&LastTransaction={request_id}&Currency=ILS&Amount=4528141.00"
    response = requests.post(url,headers=headers)
    return response
