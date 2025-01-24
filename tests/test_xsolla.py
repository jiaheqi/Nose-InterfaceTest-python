import random
from unittest import TestCase

from tests.components.httpclient import http_client
from tests.components.fake import generate_device_id
from tests.components.utils import register_user, role_save


class TestXsollaLogin(TestCase):
    def setUp(self) -> None:
        device = generate_device_id()
        user = register_user(device)
        self.account = user.get("account")
        self.user_id = user.get("id")

        self.role_id = f"{self.user_id}_1111"
        self.role_name = f"role_name_{self.user_id}"

        role_save(device, self.user_id, self.role_id, self.role_name)

    def test_xsolla_login(self):
        """[用户管理]--Xsolla用户登录"""

        path = "/xsolla/login?merchant_id=123456&project_id=654321"
        body = {
            "user": {
                "id": self.role_id,
                "country": "HK"
            }
        }

        response = http_client.post(path, body)
        self.assertEqual(response.json().get("user").get("id"), self.role_id)
        self.assertEqual(response.json().get("user").get("name"), self.role_name)


class TestXsollaPay(TestCase):
    def setUp(self) -> None:
        device = generate_device_id()
        user = register_user(device)
        self.account = user.get("account")
        self.user_id = user.get("id")

        self.role_id = f"{self.user_id}_1111"
        self.role_name = f"role_name_{self.user_id}"

        role_save(device, self.user_id, self.role_id, self.role_name)

    def test_xsolla_pay(self):
        """[支付服务]--Xsolla支付单件单个商品"""

        path = "/xsolla/pay?merchant_id=123456&project_id=654321"
        body = {
            "notification_type": "order_paid",
            "items": [
                {
                    "sku": "ring_s",
                    "type": "virtual_good",
                    "is_pre_order": False,
                    "quantity": 1,
                    "amount": "100.0000",
                    "promotions": []
                }
            ],
            "order": {
                "id": random.randint(1000000, 9999999),
                "mode": "sandbox",
                "currency_type": "real",
                "currency": "USD",
                "amount": "100.0000",
                "status": "paid",
                "platform": "xsolla",
                "comment": None,
                "invoice_id": str(random.randint(1000000, 9999999)),
                "promotions": []
            },
            "user": {
                "external_id": self.role_id,
                "Email": "test@topjoy.com"
            }
        }

        response = http_client.post(path, body)
        self.assertEqual(response.status_code, 204)

    def test_xsolla_pay_with_quantity(self):
        """[支付服务]--Xsolla支付多件单个商品"""

        path = "/xsolla/pay?merchant_id=123456&project_id=654321"
        body = {
            "notification_type": "order_paid",
            "items": [
                {
                    "sku": "ring_s",
                    "type": "virtual_good",
                    "is_pre_order": False,
                    "quantity": 2,
                    "amount": "100.0000",
                    "promotions": []
                }
            ],
            "order": {
                "id": random.randint(1000000, 9999999),
                "mode": "sandbox",
                "currency_type": "real",
                "currency": "USD",
                "amount": "100.0000",
                "status": "paid",
                "platform": "xsolla",
                "comment": None,
                "invoice_id": str(random.randint(1000000, 9999999)),
                "promotions": []
            },
            "user": {
                "external_id": self.role_id,
                "Email": "test@topjoy.com"
            }
        }

        response = http_client.post(path, body)
        self.assertEqual(response.status_code, 204)

    def test_xsolla_pay_with_multi_item(self):
        """[支付服务]--Xsolla支付单件多个商品"""

        path = "/xsolla/pay?merchant_id=123456&project_id=654321"
        body = {
            "notification_type": "order_paid",
            "items": [
                {
                    "sku": "ring_a",
                    "type": "virtual_good",
                    "is_pre_order": False,
                    "quantity": 1,
                    "amount": "100.0000",
                    "promotions": []
                },
                {
                    "sku": "ring_b",
                    "type": "virtual_good",
                    "is_pre_order": False,
                    "quantity": 1,
                    "amount": "100.0000",
                    "promotions": []
                }
            ],
            "order": {
                "id": random.randint(1000000, 9999999),
                "mode": "sandbox",
                "currency_type": "real",
                "currency": "USD",
                "amount": "100.0000",
                "status": "paid",
                "platform": "xsolla",
                "comment": None,
                "invoice_id": str(random.randint(1000000, 9999999)),
                "promotions": []
            },
            "user": {
                "external_id": self.role_id,
                "Email": "test@topjoy.com"
            }
        }

        response = http_client.post(path, body)
        self.assertEqual(response.status_code, 204)

    def test_xsolla_pay_with_multi_item_and_quantity(self):
        """[支付服务]--Xsolla支付多件多个商品"""

        path = "/xsolla/pay?merchant_id=123456&project_id=654321"
        body = {
            "notification_type": "order_paid",
            "items": [
                {
                    "sku": "ring_a",
                    "type": "virtual_good",
                    "is_pre_order": False,
                    "quantity": 1,
                    "amount": "100.0000",
                    "promotions": []
                },
                {
                    "sku": "ring_b",
                    "type": "virtual_good",
                    "is_pre_order": False,
                    "quantity": 2,
                    "amount": "100.0000",
                    "promotions": []
                }
            ],
            "order": {
                "id": random.randint(1000000, 9999999),
                "mode": "sandbox",
                "currency_type": "real",
                "currency": "USD",
                "amount": "100.0000",
                "status": "paid",
                "platform": "xsolla",
                "comment": None,
                "invoice_id": str(random.randint(1000000, 9999999)),
                "promotions": []
            },
            "user": {
                "external_id": self.role_id,
                "Email": "test@topjoy.com"
            }
        }

        response = http_client.post(path, body)
        self.assertEqual(response.status_code, 204)
