from unittest import TestCase

from tests.components.httpclient import sdk_http_client
from tests.components.tools import time_format_YmdHMS
from tests.components.utils import register_user
from zeus_client import generate_device_id


class TestHuaweiExchange(TestCase):
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

    def test_huawei_exchange(self):
        """[华为支付]创建华为订单：正常创建订单"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)
        self.assertIsNotNone(response.json().get('result').get('order_id'))

    def test_huawei_exchange_with_empty_body(self):
        """[华为支付]创建华为订单：空表单"""
        path = "/order/huawei-exchange"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_with_blank_body(self):
        """[华为支付]创建华为订单：参数为空"""
        path = "/order/huawei-exchange"
        body = {
            "description": "",
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

    def test_huawei_exchange_with_null_body(self):
        """[华为支付]创建华为订单：参数为null"""
        path = "/order/huawei-exchange"
        body = {
            "description": None,
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
        self.assertEqual(response.json().get('error_no'), 1002)

    def test_huawei_exchange_without_user_id(self):
        """[华为支付]创建华为订单：参数缺失，缺少userId"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_without_role_id(self):
        """[华为支付]创建华为订单，参数缺失，缺少roleId"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "product_id": "zeusdemo.huawei.product01",
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_without_product_id(self):
        """[华为支付]创建华为订单：参数缺失，缺少product_id"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "99",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_without_price(self):
        """[华为支付]创建华为订单：参数缺失，缺少price"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_with_invalid_price(self):
        """[华为支付]创建华为订单：参数不合法，不合法的金额：金额为字母"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "abc",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_with_invalid_price2(self):
        """[华为支付]创建华为订单：参数不合法，不合法的金额：金额为汉字"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "哈哈",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_with_invalid_price3(self):
        """[华为支付]创建华为订单：参数不合法，不合法的金额：金额为符号"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "@!#!@ ",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_exchange_with_invalid_price4(self):
        """[华为支付]创建华为订单：参数不合法，不合法的金额：金额小数位数不合法"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "0.00000000999999",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_huawei_exchange_with_invalid_price5(self):
        """[华为支付]创建华为订单：参数不合法，不合法的金额：金额为0"""
        path = "/order/huawei-exchange"
        body = {
            "description": "crystal",
            "device": self.device,
            "extend": self.current_time,
            "lang": "1",
            "level": "5",
            "pay_notify_url": "test",
            "platform": "android",
            "price": "0",
            "product_id": "zeusdemo.huawei.product01",
            "role_id": self.role_id,
            "role_name": self.role_name,
            "sdk_version": "2.5.3",
            "server_id": "1",
            "server_name": "区服名",
            "user_id": self.user_id,
            "vip": "1"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


class TestHuaweiVerify(TestCase):

    def setUp(self) -> None:
        # 测试环境
        # self.purchaseToken = "0000018a886641b3150c251296716102b18b3f3262bcfc7c9891664ec55ca75d68cfb282d079489cx434e.1" \
        #                      ".109083613"
        # self.purchase_data = "{\"autoRenewing\":false,\"orderId\":\"2023091215582789171e17cb31.109083613\"," \
        #                      "\"packageName\":\"com.topjoy.zeusdemo.huawei\",\"applicationId\":109083613," \
        #                      "\"applicationIdString\":\"109083613\",\"kind\":0," \
        #                      "\"productId\":\"zeusdemo.huawei.product01\",\"productName\":\"元宝1\"," \
        #                      "\"purchaseTime\":1694505517000,\"purchaseTimeMillis\":1694505517000," \
        #                      "\"purchaseState\":0,\"developerPayload\":\"hw_20230912155825_i77Beb\"," \
        #                      "\"purchaseToken" \
        #                      "\":\"0000018a886641b3150c251296716102b18b3f3262bcfc7c9891664ec55ca75d68cfb282d079489cx434e.1.109083613\",\"consumptionState\":0,\"confirmed\":0,\"purchaseType\":0,\"currency\":\"CNY\",\"price\":100,\"country\":\"CN\",\"payOrderId\":\"sandboxPeea335821888d0f77e7b577647d2113\",\"payType\":\"71\",\"sdkChannel\":\"1\"}"
        # self.dataSignature = "gRmkkWsIUAGTfaghVeAMYA4I07MBxauGNzTPc5TgWIh9P5+N+SRsJQsZ3Ucwb" \
        #                      "+aPqGNKEpr4AIQI5heBDuqbUZua+kF7inCjxJCiqclrcTdE9D+HbnuX1KhCDw4" \
        #                      "++DfjwSoiXDNTeMu29e6Z0zFWA6lY2PbyS+ySlXHgB7L1G2XwUO0gTb4OxPk" \
        #                      "+ijGnP4AYpglRdD8cDGPwPG3qKJWprdPKB+PVUdgpUxh5T6gF+x1b7EefPh/i80OXWUioRgUa" \
        #                      "+YMDHh2Bii7vLuq8pLkdnD7eVnMZ4tdFSaA1BiDNCzN0zDogUE4pxZaQFuJ2reV5HAo8dWHTkE6qmn85xpByotZlZuFU13DTWcQMOawIsX2hJHPBJUKBa7WEDcsTpnzJBs7KvGG7m3ar/Tg4HOxoVsjznrKjnfHFN3XQU1CwgLftVXmFMgac3iYGDVdeBT0UuurfsG3DUIH1/DKXqkd5uWF1ys8Zr9zWtEP7cCuY6dZlnSRjOkK5ikSv5yoAn3AE"
        # self.developerPayload = "hw_20230912155825_i77Beb"
        # 沙箱环境
        self.purchaseToken = "0000018b187700ef48ded97a09af80c4fbcdebb9c8bd4559608772f2088623bfaec0a40511bd14dcx434e.1.109083613"
        self.purchase_data = "{\"autoRenewing\":false,\"orderId\":\"20231010151954317dbcbac661.109083613\",\"packageName\":\"com.topjoy.zeusdemo.huawei\",\"applicationId\":109083613,\"applicationIdString\":\"109083613\",\"kind\":0,\"productId\":\"zeusdemo.huawei.product01\",\"productName\":\"元宝1\",\"purchaseTime\":1696922534000,\"purchaseTimeMillis\":1696922534000,\"purchaseState\":0,\"developerPayload\":\"hw_20231010151951_DDMi0r\",\"purchaseToken\":\"0000018b187700ef48ded97a09af80c4fbcdebb9c8bd4559608772f2088623bfaec0a40511bd14dcx434e.1.109083613\",\"consumptionState\":0,\"confirmed\":0,\"purchaseType\":0,\"currency\":\"CNY\",\"price\":100,\"country\":\"CN\",\"payOrderId\":\"sandboxPe10adc5b2e1be60f41cb844453dab13\",\"payType\":\"71\",\"sdkChannel\":\"1\"}"
        self.dataSignature = "eeLvPIJaBUSNGtrxP1DF5nhJDloRlK8y2qkjzKzFB9VBiQF81BHkRgEdTmdkiI7SfGSlniUyCcVwfZ8+pb2KEtdEaQsP0+zJQ0rpv8SPa+eBYixbofVnx5FRIPaAzRyxgqWRG8+oVvJc0xLol/7eS6EBwQy61u9sZ3Vq7WDscESa99TAy0Rv7QPWyZPIXiJxgHsX3ClawgFRL7nvLYLFt3SZv+C0qASyO4mbL/4Yj7IVDpqhyRw2du28DZULEAGd6d0Fb20/PGmnPPKFYcFJOC2+kJdcIVcLQrBosjXeikvwhI/uPw7jNSlGnBHtbdjnocUqe+Bng6Q+chzZju2uW0sV/um7HqX25dyGTthdokuTGMvMdzWIxc7uhMtyfcOY9q2c/9yZDewJqMDom9NlicyCo1sey4VYF8DvTgSHAo9YcWlLvGglSTOlM02ZnQF9YI4WEEYiIcxJygiyx5/VKrtogkE6faJsTIyLsdzLLxvcABUvvAD7vwKaYgITA57c"
        self.developerPayload = "hw_20231010151951_DDMi0r"

    def test_huawei_verify(self):
        """[华为支付]已确定订单重复确认
        """
        # dataSignature中的转译字符要去掉，否则base64.b64encode之后会默认多添加一个转义字符，导致sign生成有问题从未导致验签失败
        path = "order/huawei-verify"
        body = {
            "dataSignature": self.dataSignature,
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.zeusdemo.huawei",
            "pay_amount": "100",
            "pay_currency": "CNY",
            "platform": "android",
            "productId": "zeusdemo.huawei.product01",
            "purchaseToken": self.purchaseToken,
            "purchase_data": self.purchase_data,
            "sdk_version": "2.9.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_huawei_verify_with_empty_body(self):
        """[华为支付]空表单"""
        path = "order/huawei-verify"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_verify_with_blank_body(self):
        """[华为支付]参数为空"""
        path = "order/huawei-verify"
        body = {
            "appid": "",
            "dataSignature": "",
            "developerPayload": "",
            "lang": "",
            "packageName": "",
            "pay_amount": "",
            "pay_currency": "",
            "platform": "",
            "productId": "",
            "purchaseToken": "",
            "purchase_data": "",
            "sdk_version": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_verify_with_null_body(self):
        """[华为支付]参数为null"""
        path = "order/huawei-verify"
        body = {
            "appid": None,
            "dataSignature": None,
            "developerPayload": None,
            "lang": None,
            "packageName": None,
            "pay_amount": None,
            "pay_currency": None,
            "platform": None,
            "productId": None,
            "purchaseToken": None,
            "purchase_data": None,
            "sdk_version": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_verify_without_dataSignature(self):
        """[华为支付]参数缺失，缺少dataSignature"""
        path = "order/huawei-verify"
        body = {
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.zeusdemo.huawei",
            "pay_amount": "100",
            "pay_currency": "CNY",
            "platform": "android",
            "productId": "zeusdemo.huawei.product01",
            "purchaseToken": self.purchaseToken,
            "purchase_data": self.purchaseToken,
            "sdk_version": "2.9.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_verify_without_purchaseToken(self):
        """[华为支付]参数缺失，缺少purchaseToken"""
        path = "order/huawei-verify"
        body = {
            "appid": "7AVS2D5QH2TV",
            "dataSignature": self.dataSignature,
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.zeusdemo.huawei",
            "pay_amount": "100",
            "pay_currency": "CNY",
            "platform": "android",
            "productId": "zeusdemo.huawei.product01",
            "purchase_data": self.purchase_data,
            "sdk_version": "2.9.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_huawei_verify_without_purchase_data(self):
        """[华为支付]参数缺失，缺少purchase_data"""
        path = "order/huawei-verify"
        body = {
            "appid": "7AVS2D5QH2TV",
            "dataSignature": self.dataSignature,
            "developerPayload": self.developerPayload,
            "lang": "1",
            "packageName": "com.topjoy.zeusdemo.huawei",
            "pay_amount": "100",
            "pay_currency": "CNY",
            "platform": "android",
            "productId": "zeusdemo.huawei.product01",
            "purchaseToken": self.purchaseToken,
            "sdk_version": "2.9.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

