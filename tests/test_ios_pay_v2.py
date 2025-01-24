from unittest import TestCase

from tests.components.fake import generate_device_id, get_app_id, get_ios_transaction_id
from tests.components.httpclient import sdk_http_client
from tests.components.tools import time_format_timestamp_ms
from tests.components.utils import role_save, register_user

"""
[iosV2支付]创建ios订单
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少userId，roleId，productId，price
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求
2.返回值和类型校验
"""

"""
[iosV2支付确认]ios订单确认
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少order_id,pay_amount，transaction_id
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求TODO
2.未支付订单确认TODO
4.已支付订单重复确认
"""


class TestIosPayV2(TestCase):
    def setUp(self) -> None:
        device = generate_device_id()
        user = register_user(device)
        current_timestamp = time_format_timestamp_ms()
        self.device = device
        self.account = user.get("account")
        self.user_id = str(user.get("id"))

        self.role_id = f"{self.user_id}_1111"
        self.role_name = f"role_name_{self.user_id}"
        self.extend = str(current_timestamp)
        role_save(device, self.user_id, self.role_id, self.role_name)

    def test_order_ios_exchange(self):
        """[iosV2支付]创建支付单，正常请求"""
        path = "/v2/order/ios-exchange"
        body ={
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "0.99",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639875",
                "device": self.device,
                "role_id":  self.role_id,
            }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)
        self.assertIsNotNone(response.json().get('result').get('order_id'))
        self.assertIsInstance(response.json().get('result').get('order_id'), str)

    def test_order_ios_exchange_with_empty_body(self):
        """[iosV2支付]创建支付单，空表单"""
        path = "/v2/order/ios-exchange"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_blank_body(self):
        """[iosV2支付]创建支付单，参数为空"""
        path = "/v2/order/ios-exchange"
        body = {
            "appid": "",
            "vip": "",
            "server_name": "",
            "server_id": "",
            "user_id": "",
            "role_name": "",
            "sdk_version": "",
            "price": "",
            "platform": "",
            "product_id": "",
            "level": "",
            "pay_notify_url": "",
            "lang": "",
            "extend": "",
            "device": "",
            "role_id": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_null_body(self):
        """[iosV2支付]创建支付单，参数为null"""
        path = "/v2/order/ios-exchange"
        body = {
            "appid": None,
            "vip": None,
            "server_name": None,
            "server_id": None,
            "user_id": None,
            "role_name": None,
            "sdk_version": None,
            "price": None,
            "platform": None,
            "product_id": None,
            "level": None,
            "pay_notify_url": None,
            "lang": None,
            "extend": None,
            "device": None,
            "role_id": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_user_id(self):
        """[iosV1支付]创建支付单，参数缺失，缺少user_id"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "0.99",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
            }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_role_id(self):
        """[iosV2支付]创建支付单，参数缺失，缺少role_id"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "0.99",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_role_name(self):
        """[iosV2支付]创建支付单，参数缺失，缺少role_name"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "sdk_version": "2.8.0",
                "price": "0.99",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_product_id(self):
        """[iosV2支付]创建支付单，参数缺失，缺少product_id"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "0.99",
                "platform": "ios",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_price(self):
        """[iosV2支付]创建支付单，参数缺失，缺少price"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price(self):
        """[iosV2支付]创建支付单，金额不合法：汉字"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "哈哈",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id
            }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price2(self):
        """[iosV2支付]创建支付单，金额不合法：字母"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "abc",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
            }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price3(self):
        """[iosV2支付]创建支付单，金额不合法：符号"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "!@#$  ",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
            }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price4(self):
        """[iosV2支付]创建支付单，金额不合法：小数位数不合法"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "0.00000099",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
            }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_exchange_with_invalid_price5(self):
        """[iosV2支付]创建支付单，金额不合法：金额为0"""
        path = "/v2/order/ios-exchange"
        body = {
                "appid": get_app_id(),
                "vip": "5",
                "server_name": "玩家区服",
                "server_id": "1",
                "user_id": self.user_id,
                "role_name": self.role_name,
                "sdk_version": "2.8.0",
                "price": "0",
                "platform": "ios",
                "product_id": "com.topjoy.zeusdemo.iap1",
                "level": "12",
                "pay_notify_url": "test",
                "lang": "1",
                "extend": "serverId=3|userId=1011s3p60896|productId=121691639874",
                "device": self.device,
                "role_id":  self.role_id,
            }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


class TestIosPayV2Verify(TestCase):
    def test_order_ios_verify(self):
        """[iosV2支付确认]已成功订单重复确认"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "0.99",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_with_blank_order_id(self):
        """[iosV2支付确认]orderId为空"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "0.99",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_with_empty_body(self):
        """[iosV2支付确认]参数校验：空表单"""
        path = "/v2/order/ios-verify"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_with_blank_body(self):
        """[iosV2支付确认]参数校验：表单为空"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "",
            "pay_currency": "",
            "transaction_id": "",
            "platform": "",
            "pay_amount": "",
            "sdk_version": "",
            "appid": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_with_null_body(self):
        """[iosV2支付确认]参数校验：表单为null"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": None,
            "pay_currency": None,
            "transaction_id": None,
            "platform": None,
            "pay_amount": None,
            "sdk_version": None,
            "appid": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_without_order_id(self):
        """[iosV2支付确认]参数缺失，缺少order_id"""
        path = "/v2/order/ios-verify"
        body = {
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "0.99",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_without_pay_amount(self):
        """[iosV2支付确认]参数缺失，缺少pay_amount"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_without_transaction_id(self):
        """[iosV2支付确认]参数缺失，缺少transaction_id"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "platform": "ios",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_with_invalid_pay_amount(self):
        """[iosV2支付确认]参数不合法：金额小数位数不合法"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "0.000000099",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_with_invalid_pay_amount1(self):
        """[iosV2支付确认]参数不合法：金额为汉字"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "哈哈",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_with_invalid_pay_amount2(self):
        """[iosV2支付确认]参数不合法：金额为字母"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "abc",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_with_invalid_pay_amount3(self):
        """[iosV2支付确认]参数不合法：金额为符号"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "!@#$  ",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_with_invalid_pay_amount4(self):
        """[iosV2支付确认]参数不合法：金额为0"""
        path = "/v2/order/ios-verify"
        body = {
            "order_id": "e434bffb-51f9-471b-b85c-5d296d2bcc7b",
            "pay_currency": "USD",
            "transaction_id": get_ios_transaction_id(),
            "platform": "ios",
            "pay_amount": "0",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)
