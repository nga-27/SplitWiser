import requests

def handle_get_payload(url: str) -> dict:
    data = requests.get(url)
    if data.status_code == 200:
        return data.json()
    else:
        return {}

def handle_delete_id(url: str) -> bool:
    response = requests.delete(url)
    return response.status_code == 201

def handle_post(url: str, json_data: dict) -> None:
    response = requests.post(url, json=json_data)
    if response.status_code != 201:
        print(f"ERROR on saving post to '{url}'. Response was: {response.status_code}")
    return
