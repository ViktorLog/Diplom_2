import random
import string

import allure
import requests

from endpoints import ApiEndpoints


def random_text(length=15):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def make_account_data():
    return {
        "email": "qa_" + random_text() + "@example.com",
        "password": random_text(),
        "name": random_text(),
    }


@allure.step("Удалить созданного тестового пользователя")
def remove_account(account_payload):
    response = send_login({
        "email": account_payload["email"],
        "password": account_payload["password"],
    })
    if response.status_code == 401:
        return
    response.raise_for_status()
    token = response.json()["accessToken"]
    response = requests.delete(
        ApiEndpoints.USER_URL, headers={"Authorization": token}, timeout=30
    )
    response.raise_for_status()


@allure.step('Отправить запрос на оформление заказа')
def send_order(ingredients, token=None):
    headers = {"Authorization": token} if token else {}
    return requests.post(
        ApiEndpoints.ORDERS_URL, json={"ingredients": ingredients}, headers=headers, timeout=45
    )


@allure.step('Отправить запрос регистрации')
def send_registration(payload):
    return requests.post(ApiEndpoints.REGISTER_URL, json=payload, timeout=30)


@allure.step('Выполнить запрос входа')
def send_login(credentials):
    return requests.post(ApiEndpoints.LOGIN_URL, json=credentials, timeout=30)


@allure.step("Загрузить список ингредиентов для подготовки заказа")
def fetch_ingredients():
    response = requests.get(ApiEndpoints.INGREDIENTS_URL, timeout=30)
    response.raise_for_status()
    return response.json()["data"]
