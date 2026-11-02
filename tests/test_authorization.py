import allure
import pytest

from messages import ApiMessages
from helpers import random_text
from helpers import send_login


class TestAuthorization:

    @allure.title('Вход с данными зарегистрированного аккаунта')
    def test_registered_account_can_sign_in(self, created_account):
        response = send_login({key: created_account[key] for key in ["email", "password"]})

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": created_account["email"], "name": created_account["name"]}
        assert body["accessToken"]
        assert body["refreshToken"]

    @allure.title('Ошибка входа с неверным email или паролем')
    @pytest.mark.parametrize('field_name', ["email", "password"])
    def test_incorrect_credentials_are_rejected(self, created_account, field_name):
        credentials = {key: created_account[key] for key in ["email", "password"]}
        credentials[field_name] = random_text() + ("@example.com" if field_name == "email" else "")

        response = send_login(credentials)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": ApiMessages.INVALID_CREDENTIALS}
