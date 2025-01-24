from unittest import TestCase

from tests.components.httpclient import tkw_http_client
"""
[tkwPay]查询用户信息
[tkwPay]下单
[tkwPay]支付完成页面跳转
"""


class TestTkwPayUser(TestCase):
    def test_tkw_check_user(self):
        """[tkwPay]查询用户信息"""
        path = "/check_user"
        body = {
            "role_id": "10002"
        }
        response = tkw_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result')[0].get('level'))
        self.assertIsNotNone(response.json().get('result')[0].get('role_id'))
        self.assertIsNotNone(response.json().get('result')[0].get('role_name'))
        self.assertIsNotNone(response.json().get('result')[0].get('server_id'))
        self.assertIsNotNone(response.json().get('result')[0].get('server_name'))
        self.assertIsInstance(response.json().get('result')[0].get('level'), str)
        self.assertIsInstance(response.json().get('result')[0].get('role_id'), str)
        self.assertIsInstance(response.json().get('result')[0].get('role_name'), str)
        self.assertIsInstance(response.json().get('result')[0].get('server_id'), str)
        self.assertIsInstance(response.json().get('result')[0].get('server_name'), str)


# class TestTkwPayOrder(TestCase):
#     """[tkwPay]下单，正常请求"""
#     def test_tkw_pay(self):
#         path = "/order"
#         body = {
#             "region": "tw",
#             "currency": "TWD",
#             "role_id": "10002",
#             "product_id": "mycardid_6",
#             "server_id": "80002",
#             "pay_way": 8
#         }
#         response = tkw_http_client.post(path, body)
#         self.assertEqual(response.json().get('code'), 0)
#         self.assertIsNotNone(response.json().get('result').get('pay_url'))
#         self.assertIsInstance(response.json().get('result').get('pay_url'), str)


class TestTkwPayNotify(TestCase):
    def test_tkw_pay(self):
        """[tkwPay]支付完成回调跳转"""
        path = "/pay_return"
        body = {
            "merchant_id": "zeus2023",
            "pay_way": 8
        }
        # 支付完成后跳转到支付完成页面
        response = tkw_http_client.post(path, body)
        self.assertIsNotNone(response.text)
