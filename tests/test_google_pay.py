from unittest import TestCase

from tests.components.fake import generate_device_id, get_app_id
from tests.components.httpclient import sdk_http_client
from tests.components.tools import time_format_YmdHMS
from tests.components.utils import register_user

"""
[google支付]创建Google订单
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少userId，roleId，productId，price
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求
2.校验返回值和类型
"""
"""
[google支付确认]google订单确认
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少developerPayload，pay_amount，purchaseToken，purchase_data，purchase_sign
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求TODO
2.未支付订单确认
4.已支付订单重复确认
"""


class TestGooglePay(TestCase):

    def setUp(self) -> None:
        device = generate_device_id()
        user = register_user(device)
        current_time = time_format_YmdHMS()
        self.current_time = current_time
        self.device = device
        self.account = user.get("account")
        self.user_id = str(user.get("id"))

        self.role_id = f"{self.user_id}_1111"
        self.role_name = f"role_name_{self.user_id}"

    def test_google_exchange(self):
        """[google支付]创建Google订单：正常请求"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)
        self.assertEqual(response.json().get('error_no'), 0)
        self.assertIsNotNone(response.json().get('result').get('order_id'))
        self.assertIsInstance(response.json().get('result').get('google_pay_key'), str)
        self.assertIsInstance(response.json().get('result').get('order_id'), str)

    def test_google_exchange_with_empty_body(self):
        """[google支付]创建Google订单：空表单"""
        path = "/order/google-exchange"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_with_blank_body(self):
        """[google支付]创建Google订单：参数为空"""
        path = "/order/google-exchange"
        body = {
            "appid": "",
            "device": "",
            "extend": "",
            "lang": "",
            "level": "",
            "pay_notify_url": "",
            "platform": "",
            "price": "",
            "product_id": "",
            "role_id": "",
            "role_name": "",
            "sdk_version": "",
            "server_id": "",
            "server_name": "",
            "user_id": "",
            "vip": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_with_null_body(self):
        """[google支付]创建Google订单：参数为null"""
        path = "/order/google-exchange"
        body = {
            "appid": None,
            "device": None,
            "extend": None,
            "lang": None,
            "level": None,
            "pay_notify_url": None,
            "platform": None,
            "price": None,
            "product_id": None,
            "role_id": None,
            "role_name": None,
            "sdk_version": None,
            "server_id": None,
            "server_name": None,
            "user_id": None,
            "vip": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_without_user_id(self):
        """[google支付]创建Google订单：参数缺失，缺少userId"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_without_role_id(self):
        """[google支付]创建Google订单，参数缺失，缺少roleId"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_without_product_id(self):
        """[google支付]创建Google订单：参数缺失，缺少product_id"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_without_price(self):
        """[google支付]创建Google订单：参数缺失，缺少price"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_with_invalid_price(self):
        """[google支付]创建Google订单：参数不合法，不合法的金额：金额为字母"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "abc",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_with_invalid_price2(self):
        """[google支付]创建Google订单：参数不合法，不合法的金额：金额为汉字"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "哈哈",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_with_invalid_price3(self):
        """[google支付]创建Google订单：参数不合法，不合法的金额：金额为符号"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "@!#!@ ",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_exchange_with_invalid_price4(self):
        """[google支付]创建Google订单：参数不合法，不合法的金额：金额小数位数不合法"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "0.00000000999999",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_google_exchange_with_invalid_price5(self):
        """[google支付]创建Google订单：参数不合法，不合法的金额：金额为0"""
        path = "/order/google-exchange"
        body = {
            "appid": get_app_id(),
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "0",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.4-SNAPSHOT",
            "server_id": "1",
            "server_name": "serverName",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


class TestGoogleVerify(TestCase):
    def setUp(self) -> None:
        # 沙箱环境
        self.purchaseToken = "eakpihfilaobljpcanbgnaaj.AO-J1Ox1D1ony1pbbcf_i9Dd1lji9IL_q1lMgf3McOr1kRSB2DBs8QwCAKDyXCVEQ5sOhbY1TLSVQcjZDnEXjcgGzoURiXdSwA"
        self.purchase_data = "{\"orderId\":\"GPA.3330-5464-9384-40093\",\"packageName\":\"com.topjoy.sdk_demo\",\"productId\":\"com.topjoy.sdk_demo.pay100\",\"purchaseTime\":1691573700210,\"purchaseState\":0,\"purchaseToken\":\"eakpihfilaobljpcanbgnaaj.AO-J1Ox1D1ony1pbbcf_i9Dd1lji9IL_q1lMgf3McOr1kRSB2DBs8QwCAKDyXCVEQ5sOhbY1TLSVQcjZDnEXjcgGzoURiXdSwA\",\"obfuscatedAccountId\":\"a_20230809173454_qkBydI\",\"quantity\":1,\"acknowledged\":false,\"developerPayload\":\"a_20230809173454_qkBydI\"}"
        self.purchase_sign = "UTQUfVLKwDKuOLcCiBVrjd5cI0Zk7o0g5kiLZx7VkMp5mtrApHm8f6EtrNLNjmZ1aLeLGsFZzCm+dPobW9wvdbf9+FzxDONR+tSPeBDGS\/jrACkUI4j\/JDD9f0MB8HZpx3kEpZGoCZS0froSQTYh7aYnsrOHGpfinQI\/rYePQkr1467rUEDsKrlNMZFU1ILklv0RsV6ScVlq2JMq+4wALO16OzB5lW88x9xk1YVd59ZDXTIM67\/7svA39vSXGKy\/QcZmExBRcAbc\/idf+CiZ4z\/7MrmT3jM3jtsIVBmzm4+f3vi5GPrpD0VRsyiLEo1ZB8\/MBoeOYdldV6mLeeSUXA=="
        self.developerPayload = "a_20230809173454_qkBydI"
        # 测试环境
        # self.purchaseToken = "enjkojphepifgalciebaigdn.AO-J1OyfmrOCxfDJNBzCUDRmYikgok8io4GH8QR8izEf_QsgkhoXxgKF6RKb2bDnmiIDBz8oKWhcTfDwzhxQW11o1encVmxLoQ"
        # self.purchase_data =  "{\"orderId\":\"GPA.3339-4507-1651-50011\",\"packageName\":\"com.topjoy.sdk_demo\",\"productId\":\"com.topjoy.sdk_demo.pay100\",\"purchaseTime\":1692343154444,\"purchaseState\":0,\"purchaseToken\":\"enjkojphepifgalciebaigdn.AO-J1OyfmrOCxfDJNBzCUDRmYikgok8io4GH8QR8izEf_QsgkhoXxgKF6RKb2bDnmiIDBz8oKWhcTfDwzhxQW11o1encVmxLoQ\",\"obfuscatedAccountId\":\"a_20230818151907_C04z8e\",\"quantity\":1,\"acknowledged\":false,\"developerPayload\":\"a_20230818151907_C04z8e\"}"
        # self.purchase_sign = "MNUzEbVrwNjV1E9nk9ZkDJxauATjHEbOtMfOXJWg7t2kGkRuv3r9MtxUhmNM+LeN\/bsnejgIm9lGGmmwnlfxDXatSaAZVTIRq7bNAgWFmlVHw+vAbg+7RKnM1yxqTppJxcGV2kgQL91LL8Uforyehbao42BlNYrKUNJUZF46lPk0xO5HU38Px1JXQJgvTTQMQmFUIn8JYo0qbmeeadTpJHUoyR9FHC35naonW8LkqqSrPgAOUTk7Kk1bUwnOBSdWtIhw14\/P5ls0xChS7hkHR6YhV4IRuAvBykQjPuUlbG24bL7j4oEewGwU9frqQ134nNCS7jsTx5dV\/qI\/Cf8xlw=="
        # self.developerPayload = "a_20230818151907_C04z8e"

    def test_google_verify(self):
        """[google支付确认]，已完成订单重复确认"""
        path = "v2/order/google-verify"
        body = {
            "appid": get_app_id(),
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.sdk_demo",
            "pay_amount": "1.49",
            "pay_currency": "USD",
            "platform": "android",
            "productId": "com.topjoy.sdk_demo.pay100",
            "purchaseToken": self.purchaseToken,
            "purchase_data": self.purchase_data,
            "purchase_sign": self.purchase_sign,
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_google_verify_with_empty_body(self):
        """[google支付确认]参数校验，空表单"""
        path = "v2/order/google-verify"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_verify_with_blank_body(self):
        """[google支付确认]参数校验，参数为空"""
        path = "v2/order/google-verify"
        body = {
            "appid": "",
            "developerPayload": "",
            "lang": "",
            "packageName": "",
            "pay_amount": "",
            "pay_currency": "",
            "platform": "",
            "productId": "",
            "purchaseToken": "",
            "purchase_data": "",
            "purchase_sign": "",
            "sdk_version": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_verify_with_null_body(self):
        """[google支付确认]参数校验，参数为null"""
        path = "v2/order/google-verify"
        body = {
            "appid": None,
            "developerPayload": None,
            "lang": None,
            "packageName": None,
            "pay_amount": None,
            "pay_currency": None,
            "platform": None,
            "productId": None,
            "purchaseToken": None,
            "purchase_data": None,
            "purchase_sign": None,
            "sdk_version": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_verify_without_product_id(self):
        """[google支付确认]参数缺失，缺少product_id"""
        path = "v2/order/google-verify"
        body = {
            "appid": get_app_id(),
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.sdk_demo",
            "pay_amount": "1.49",
            "pay_currency": "USD",
            "platform": "android",
            "purchaseToken": self.purchaseToken,
            "purchase_data": self.purchase_data,
            "purchase_sign": self.purchase_sign,
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_verify_without_developerPayload(self):
        """[google支付确认]参数缺失，缺少developerPayload"""
        path = "v2/order/google-verify"
        body = {
            "appid": get_app_id(),
            "lang": "1",
            "packageName": "com.topjoy.sdk_demo",
            "pay_amount": "1.49",
            "pay_currency": "USD",
            "platform": "android",
            "productId": "com.topjoy.sdk_demo.pay100",
            "purchaseToken": self.purchaseToken,
            "purchase_data": self.purchase_data,
            "purchase_sign": self.purchase_sign,
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_verify_without_purchaseToken(self):
        """[google支付确认]参数缺失，缺少purchaseToken"""
        path = "v2/order/google-verify"
        body = {
            "appid": get_app_id(),
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.sdk_demo",
            "pay_amount": "1.49",
            "pay_currency": "USD",
            "platform": "android",
            "productId": "com.topjoy.sdk_demo.pay100",
            "purchase_data": self.purchase_data,
            "purchase_sign": self.purchase_sign,
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_google_verify_without_purchase_data(self):
        """[google支付确认]参数缺失，缺少purchase_data"""
        path = "v2/order/google-verify"
        body = {
            "appid": get_app_id(),
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.sdk_demo",
            "pay_amount": "1.49",
            "pay_currency": "USD",
            "platform": "android",
            "productId": "com.topjoy.sdk_demo.pay100",
            "purchaseToken": self.purchaseToken,
            "purchase_sign": self.purchase_sign,
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)
