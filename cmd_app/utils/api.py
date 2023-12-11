import requests
from typing import Union


def handle_get_payload(url: str, skip_response: bool = False) -> dict:
    data = requests.get(url)
    if data.status_code == 200 and not skip_response:
        return data.json()
    else:
        return {}

def handle_delete_id(url: str) -> Union[dict, None]:
    response = requests.delete(url)
    if response.status_code != 201:
        return None
    return response.json()

def handle_post(url: str, json_data: dict) -> None:
    response = requests.post(url, json=json_data)
    if response.status_code != 201:
        print(f"ERROR on saving post to '{url}'. Response was: {response.status_code}")
    return
