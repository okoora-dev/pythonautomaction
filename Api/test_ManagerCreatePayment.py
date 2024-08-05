import requests
from pytest import mark


@mark.api_test
def test_ManagerCreatePayment(manager_data_test, get_tomorrow_date):
    authorization = manager_data_test['Autho']
    url_path = manager_data_test["demo_path"]
    beneficiaryId = "c52f5054-daa4-4129-bcc6-ed0a33cdde9d"

    url = f"{url_path}/api/Payment/CreateNewPaymentRequest?beneficiaryId={beneficiaryId}&amount=535&currency=USD"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization}"
    }
    response = requests.post(url, headers=headers)
    complete_req = response.json()
    print(complete_req['requestId'])
    requestId = complete_req['requestId']
    url = f"{url_path}/api/Payment/CompletePaymentRequest?requestId={requestId}&isWithdrawal=false&invoiceFileList="
    response = requests.post(url, headers=headers)
    assert response.status_code == 403
    assert response.reason == "Forbidden"
