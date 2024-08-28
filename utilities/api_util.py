import allure
import requests

MAIN_URL = "http://ec2-54-254-162-245.ap-southeast-1.compute.amazonaws.com:9000/items"
result = requests.get(MAIN_URL)


@allure.step("Get item: {item_id}")
def get_item(item_id):
    item_url = MAIN_URL + f"/{item_id}"
    response = requests.get(item_url)
    assert response.status_code == 200
    return response.json()


@allure.step("Post item {name}-{description}-{price}-{item_type}")
def post_item(name: str, description: str, price: int, item_type: str):
    payload = {
              "name": name,
              "description": description,
              "price": price,
              "item_type": item_type
            }
    response = requests.post(MAIN_URL, json=payload)
    print(response)
    return response.json()["id"]

