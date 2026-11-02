import allure
import pytest

from messages import ApiMessages
from helpers import send_registration


class TestRegistration:

    @allure.title('Регистрация нового аккаунта возвращает данные и токены')
    def test_new_account_is_registered(self, account_data):
        response = send_registration(account_data)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": account_data["email"], "name": account_data["name"]}
        assert body["accessToken"]
        assert body["refreshToken"]

    @allure.title('Повторная регистрация отклоняется')
    def test_duplicate_account_is_rejected(self, created_account):
        payload = {key: created_account[key] for key in ["email", "password", "name"]}
        response = send_registration(payload)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": ApiMessages.USER_ALREADY_EXISTS}

    @allure.title('Регистрация с пустым обязательным полем возвращает ошибку')
    @pytest.mark.parametrize('field_name', ["email", "password", "name"])
    def test_empty_required_field_is_rejected(self, account_data, field_name):
        payload = account_data.copy()
        payload[field_name] = ""

        response = send_registration(payload)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": ApiMessages.REQUIRED_FIELDS}
