import allure

from messages import ApiMessages
from helpers import send_order


class TestOrders:

    @allure.title('Заказ с ингредиентами и токеном получает номер')
    def test_authorized_order_returns_number(self, created_account, burger_ingredients):
        response = send_order(burger_ingredients, created_account["accessToken"])

        assert response.status_code == 200
        body = response.json()
        order_number = body["order"]["number"]
        assert body["success"] is True
        assert isinstance(order_number, int)
        assert order_number > 0

    @allure.title('Для заказа без токена ожидается отказ')
    def test_guest_order_is_rejected(self, burger_ingredients):
        response = send_order(burger_ingredients)

        assert response.status_code == 401

    @allure.title('Пустой состав заказа возвращает ошибку')
    def test_empty_order_returns_error(self, created_account):
        response = send_order([], created_account["accessToken"])

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": ApiMessages.NO_INGREDIENTS}

    @allure.title('Заказ с неизвестным хешем не принимается')
    def test_unknown_ingredient_hash_returns_error(self, created_account):
        response = send_order(["invalid_hash"], created_account["accessToken"])

        assert response.status_code == 500
