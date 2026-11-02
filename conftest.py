import pytest

from helpers import remove_account, make_account_data, send_registration, fetch_ingredients


@pytest.fixture
def account_data():
    account_payload = make_account_data()
    yield account_payload
    remove_account(account_payload)


@pytest.fixture
def created_account(account_data):
    response = send_registration(account_data)
    response.raise_for_status()
    account_payload = account_data.copy()
    account_payload["accessToken"] = response.json()["accessToken"]
    return account_payload


@pytest.fixture
def burger_ingredients():
    ingredients = fetch_ingredients()
    bun = None
    filling = None
    for item in ingredients:
        if item["type"] == "bun" and bun is None:
            bun = item["_id"]
        if item["type"] == "main" and filling is None:
            filling = item["_id"]
    if bun is None or filling is None:
        raise ValueError("Не удалось подготовить состав заказа: нет булки или начинки")
    return [bun, filling, bun]
