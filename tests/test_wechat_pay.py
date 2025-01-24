from unittest import TestCase

from tests.components.fake import generate_device_id, get_app_id
from tests.components.httpclient import sdk_http_client
from tests.components.tools import time_format_timestamp_ms
from tests.components.utils import role_save, register_user
"""
[微信支付]创建微信支付订单
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少userId，roleId，roleName，productId，price
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求
2.返回值和类型校验
"""

"""
[微信支付确认]微信支付订单确认
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少order_id
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求
2.未支付订单确认TODO
4.已支付订单重复确认
"""


class TestWechatPay(TestCase):
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

    def test_wechat_pay(self):
        """[微信支付]订单创建，正常请求"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "1",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)
        self.assertIsNotNone(response.json().get('result').get('prepayId'))
        self.assertIsNotNone(response.json().get('result').get('partnerId'))
        self.assertIsNotNone(response.json().get('result').get('order_id'))
        self.assertIsNotNone(response.json().get('result').get('nonceStr'))
        self.assertIsNotNone(response.json().get('result').get('package'))
        self.assertIsNotNone(response.json().get('result').get('sign'))
        self.assertIsInstance(response.json().get('result').get('prepayId'), str)
        self.assertIsInstance(response.json().get('result').get('partnerId'), str)
        self.assertIsInstance(response.json().get('result').get('order_id'), str)
        self.assertIsInstance(response.json().get('result').get('nonceStr'), str)
        self.assertIsInstance(response.json().get('result').get('package'), str)
        self.assertIsInstance(response.json().get('result').get('sign'), str)

    def test_wechat_pay_with_empty_body(self):
        """[微信支付]订单创建，空表单"""
        path = "/order/wechat-exchange"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_with_blank_body(self):
        """[微信支付]订单创建，参数为空"""
        path = "/order/wechat-exchange"
        body = {
            "appid": "",
            "description": "",
            "device": "",
            "extend": "",
            "lang": "",
            "level": "",
            "platform": "",
            "price": "",
            "product_id": "",
            "role_id": "",
            "role_name": "",
            "sdk_version": "",
            "server_id": "",
            "server_name": "",
            "user_id": "",
            "vip": "",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_with_blank_body(self):
        """[微信支付]订单创建，参数为null"""
        path = "/order/wechat-exchange"
        body = {
            "appid": None,
            "description": None,
            "device": None,
            "extend": None,
            "lang": None,
            "level": None,
            "platform": None,
            "price": None,
            "product_id": None,
            "role_id": None,
            "role_name": None,
            "sdk_version": None,
            "server_id": None,
            "server_name": None,
            "user_id": None,
            "vip": None,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_without_product_id(self):
        """[微信支付]订单创建，参数缺失，缺少product_id"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "1",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_without_role_id(self):
        """[微信支付]订单创建，参数缺失，缺少role_id"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "1",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_without_role_name(self):
        """[微信支付]订单创建，参数缺失，缺少role_name"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "1",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_without_user_id(self):
        """[微信支付]订单创建，参数缺失，缺少user_id"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "1",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_without_price(self):
        """[微信支付]订单创建，参数缺失，缺少price"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_with_invalid_price(self):
        """[微信支付]订单创建，参数不合法，金额为汉字"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "哈哈",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_with_invalid_price1(self):
        """[微信支付]订单创建，参数不合法，金额为字母"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "abc",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_with_invalid_price2(self):
        """[微信支付]订单创建，参数不合法，金额为符号"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "!@#  ",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_pay_with_invalid_price3(self):
        """[微信支付]订单创建，参数不合法，金额小数位数不合法"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "9.0000099999",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_wechat_pay_with_invalid_price4(self):
        """[微信支付]订单创建，参数不合法，金额为0"""
        path = "/order/wechat-exchange"
        body = {
            "appid": get_app_id(),
            "description": "crystal",
            "device": self.device,
            "extend": self.extend,
            "lang": "1",
            "level": "5",
            "platform": "android",
            "price": "0",
            "product_id": "com.topjoy.sdk_demo.pay100",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


class TestWechatVerify(TestCase):
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

    def test_wechat_verify(self):
        """[支付宝支付]已支付费订单重复确认"""
        path = "/order/wechat-verify"
        body = {
            "appid": get_app_id(),
            "order_id": "w_20230810184438_ok2s5c",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_wechat_verify_with_empty_body(self):
        """[微信支付]订单确认，空表单"""
        path = "/order/wechat-verify"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_verify_with_blank_body(self):
        """[微信支付]订单确认，参数为空"""
        path = "/order/wechat-verify"
        body = {
            "appid": "",
            "order_id": "",
            "platform": "",
            "sdk_version": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_verify_with_null_body(self):
        """[微信支付]订单确认，参数为null"""
        path = "/order/wechat-verify"
        body = {
            "appid": None,
            "order_id": None,
            "platform": None,
            "sdk_version": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_verify_without_order_id(self):
        """[微信支付]参数缺失，缺少order_id"""
        path = "/order/wechat-verify"
        body = {
            "appid": get_app_id(),
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_wechat_verify_with_blank_order_id(self):
        """[微信支付]参数不合法，order_id为空"""
        path = "/order/wechat-verify"
        body = {
            "appid": get_app_id(),
            "order_id": "",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

