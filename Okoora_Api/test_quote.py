import time

import requests
from get_options import get_quote_option
from pytest import mark

@mark.regression
def test_get_quote(get_path,get_header_data):
    path = get_path
    headers = get_header_data
    pair_list = get_quote_option()
    for pair in pair_list:
        time.sleep(1)
        url = f"{path}/api/v1/Quote?buyCurrency={pair[0]}&sellCurrency={pair[1]}"
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            response_data = response.json()
            assert response_data['title'] == 'Too many requests',f"failed for payload: {response_data['title']}"
            assert response_data['detail'] == 'You have exceeded the rate limit for requests for this feature.',f"failed for payload: {response_data['detail']}"
        else:
            assert response.status_code == 200,f"failed for payload: {response.text}"
