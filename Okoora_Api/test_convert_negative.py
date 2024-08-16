import itertools
import time
from pytest import mark, param
import requests

def get_payload_options():
    """
    Generate a list of payload options for negative testing.
    """
    options = ["IL", "DDD", "-100", ""]
    matrix = [list(pair) for pair in itertools.product(options, repeat=4)]
    payloads = []
    for item in matrix:
        payloads.append({
            "buy": {
                "currency": item[0],
                "amount": item[1]
            },
            "charge": {
                "currency": item[2],
                "amount": item[3]
            }
        })
    return payloads

@mark.regression
@mark.parametrize("payload", get_payload_options())
def test_negative_convert(get_path, get_header_data, payload):
    """
    Test negative scenarios for the convert request.
    """
    path = get_path
    headers = get_header_data

    convert_response = send_convert_request(path, headers, payload)
    assert convert_response.status_code != 200, f"Failed for payload: {payload}"


def send_convert_request(path, headers, payload):
    """
    Send a convert request to the specified path with given headers and payload.
    """
    url = f"{path}/api/v1/Convert/ConvertRequest"
    try:
        response = requests.post(url, json=payload, headers=headers)
    except requests.RequestException as e:
        response = e.response
    return response

