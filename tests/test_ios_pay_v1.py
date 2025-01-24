from unittest import TestCase

from tests.components.fake import generate_device_id, get_app_id
from tests.components.httpclient import sdk_http_client
from tests.components.tools import time_format_timestamp_ms
from tests.components.utils import role_save, register_user

"""
[iosV1支付]创建ios订单
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
[iosV1支付确认]ios订单确认
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少order_id,pay_amount，paper
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求
2.未支付订单确认TODO
4.已支付订单重复确认
"""


class TestIosPayV1(TestCase):
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
        """[iosV1支付]创建支付单，正常请求"""
        path = "/order/ios-exchange"
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
            "extend": "serverId=3|userId=1011s3p60896|productId=121691639875",
            "device": self.device,
            "role_id": self.role_id,
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)
        self.assertIsNotNone(response.json().get('result').get('order_id'))
        self.assertIsInstance(response.json().get('result').get('order_id'), str)

    def test_order_ios_exchange_with_empty_body(self):
        """[iosV1支付]创建支付单，空表单"""
        path = "/order/ios-exchange"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_blank_body(self):
        """[iosV1支付]创建支付单，参数为空"""
        path = "/order/ios-exchange"
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
        """[iosV1支付]创建支付单，参数为null"""
        path = "/order/ios-exchange"
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
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_role_id(self):
        """[iosV1支付]创建支付单，参数缺失，缺少role_id"""
        path = "/order/ios-exchange"
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
                "device": self.device

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_role_name(self):
        """[iosV1支付]创建支付单，参数缺失，缺少role_name"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_product_id(self):
        """[iosV1支付]创建支付单，参数缺失，缺少product_id"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_without_price(self):
        """[iosV1支付]创建支付单，参数缺失，缺少price"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price(self):
        """[iosV1支付]创建支付单，金额不合法：汉字"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price2(self):
        """[iosV1支付]创建支付单，金额不合法：字母"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price3(self):
        """[iosV1支付]创建支付单，金额不合法：符号"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_exchange_with_invalid_price4(self):
        """[iosV1支付]创建支付单，金额不合法：小数位数不合法"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id

        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_exchange_with_invalid_price5(self):
        """[iosV1支付]创建支付单，金额不合法：金额为0"""
        path = "/order/ios-exchange"
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
                "role_id": self.role_id
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


class TestIosPayV1Verify(TestCase):
    def setUp(self) -> None:
        # 沙箱环境
        self.paper = "ewoJInNpZ25hdHVyZSIgPSAiQkEyWjBiS3VvRktlR1p3NG8rOWFpUU15OW5xbVVndEJyUzkyYk41Z004dFVjUzI2MmxNdnBtZWpWbGJxcjJTRGJXbkdVbmFPckpUQU1kV3p4aHZrMWovYUV4Qm5TazJkRG5oWjVZYkRBRVFLcVRTVjM1RFgyMFJ3VC94amtZTUpJVS9IZ3V5VER0eEFrbkxsNkJNWHhqUFNkcHorWlM2dHljMHFNcjJLVEhXT25pNk5xbWc4ZXhxNEVkcXFoQjFtZFhOM2dUY0tRQ2pxSk4rdWhjRWFsVk1DbkdrU3JmNTYranhWeWowdmZQbW1xWFpGT0ovSGgwaUNLQXlaVFVCKzhtRFhEdWg5U1NSYjM4NUpuOW9xby9kdit3YmlqNm1aeVZlRjZwYXFPenVqOE9HOCtSaU05dENLb3FPV2VXQXBaNnQySGJLV0Jsa1BVUnkzN3pQdHJFUUFBQVhLTUlJRnhqQ0NCSzZnQXdJQkFnSVFGZWVmemxKVkNtVUJmSkhmNU82eldUQU5CZ2txaGtpRzl3MEJBUXNGQURCMU1VUXdRZ1lEVlFRREREdEJjSEJzWlNCWGIzSnNaSGRwWkdVZ1JHVjJaV3h2Y0dWeUlGSmxiR0YwYVc5dWN5QkRaWEowYVdacFkyRjBhVzl1SUVGMWRHaHZjbWwwZVRFTE1Ba0dBMVVFQ3d3Q1J6VXhFekFSQmdOVkJBb01Da0Z3Y0d4bElFbHVZeTR4Q3pBSkJnTlZCQVlUQWxWVE1CNFhEVEl5TURrd01qRTVNVE0xTjFvWERUSTBNVEF3TVRFNU1UTTFObG93Z1lreE56QTFCZ05WQkFNTUxrMWhZeUJCY0hBZ1UzUnZjbVVnWVc1a0lHbFVkVzVsY3lCVGRHOXlaU0JTWldObGFYQjBJRk5wWjI1cGJtY3hMREFxQmdOVkJBc01JMEZ3Y0d4bElGZHZjbXhrZDJsa1pTQkVaWFpsYkc5d1pYSWdVbVZzWVhScGIyNXpNUk13RVFZRFZRUUtEQXBCY0hCc1pTQkpibU11TVFzd0NRWURWUVFHRXdKVlV6Q0NBU0l3RFFZSktvWklodmNOQVFFQkJRQURnZ0VQQURDQ0FRb0NnZ0VCQUx4RXpndXRhakIycjhBSkREUjZHV0h2dlNBTjlmcERuaFAxclBNOGt3N1haWnQwd2xvM0oxVHdqczFHT29MTWRiOFM0QXNwN2xocm9PZENLdmVIQUoraXpLa2k1bTNvRGVmTEQvVFFaRnV6djQxanpjS2JZckFwMTk3QW80MnRHNlQ0NjJqYmM0WXVYOHk3SVgxcnVEaHVxKzhpZzBnVDlrU2lwRWFjNVdMc2REdC9ONVNpZG1xSUlYc0VmS0hUczU3aU5XMm5qbyt3NDJYV3lETWZUbzZLQSt6cHZjd2Z0YWVHamdUd2tPKzZJWTV0a21KeXdZblFtUDdqVmNsV3hqUjAvdlFlbWtOd1lYMStoc0o1M1ZCMTNRaXc1S2kxZWpaOWwvejVTU0FkNXhKaXFHWGFQQlpZL2laUmo1RjVxejFidS9rdTB6dFNCeGd3NTM4UG1POENBd0VBQWFPQ0Fqc3dnZ0kzTUF3R0ExVWRFd0VCL3dRQ01BQXdId1lEVlIwakJCZ3dGb0FVR1l1WGpVcGJZWGhYOUtWY05SS0tPUWpqc0hVd2NBWUlLd1lCQlFVSEFRRUVaREJpTUMwR0NDc0dBUVVGQnpBQ2hpRm9kSFJ3T2k4dlkyVnlkSE11WVhCd2JHVXVZMjl0TDNkM1pISm5OUzVrWlhJd01RWUlLd1lCQlFVSE1BR0dKV2gwZEhBNkx5OXZZM053TG1Gd2NHeGxMbU52YlM5dlkzTndNRE10ZDNka2NtYzFNRFV3Z2dFZkJnTlZIU0FFZ2dFV01JSUJFakNDQVE0R0NpcUdTSWIzWTJRRkJnRXdnZjh3TndZSUt3WUJCUVVIQWdFV0syaDBkSEJ6T2k4dmQzZDNMbUZ3Y0d4bExtTnZiUzlqWlhKMGFXWnBZMkYwWldGMWRHaHZjbWwwZVM4d2djTUdDQ3NHQVFVRkJ3SUNNSUcyRElHelVtVnNhV0Z1WTJVZ2IyNGdkR2hwY3lCalpYSjBhV1pwWTJGMFpTQmllU0JoYm5rZ2NHRnlkSGtnWVhOemRXMWxjeUJoWTJObGNIUmhibU5sSUc5bUlIUm9aU0IwYUdWdUlHRndjR3hwWTJGaWJHVWdjM1JoYm1SaGNtUWdkR1Z5YlhNZ1lXNWtJR052Ym1ScGRHbHZibk1nYjJZZ2RYTmxMQ0JqWlhKMGFXWnBZMkYwWlNCd2IyeHBZM2tnWVc1a0lHTmxjblJwWm1sallYUnBiMjRnY0hKaFkzUnBZMlVnYzNSaGRHVnRaVzUwY3k0d01BWURWUjBmQkNrd0p6QWxvQ09nSVlZZmFIUjBjRG92TDJOeWJDNWhjSEJzWlM1amIyMHZkM2RrY21jMUxtTnliREFkQmdOVkhRNEVGZ1FVSXNrOGUyTVRoYjQ2TzhVenFiVDZzYkNDa3hjd0RnWURWUjBQQVFIL0JBUURBZ2VBTUJBR0NpcUdTSWIzWTJRR0N3RUVBZ1VBTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElCQVFBOFJ1N1BxRHk0L1o2RHkxSHc5cWhSL09JSEhZSWszTzZTaWh2cVRhanFPMCtITXBvNU9kdGIrRnZhVFkzTit3bEtDN0hObWhsdlRzZjlhRnM3M1BsWGo1TWtTb1IwamFBa1ozYzVnamtOank5OGdZRVA3ZXRiK0hXMC9QUGVsSkc5VElVY2ZkR09aMlJJZ2dZS3NHRWt4UEJRSzFaYXJzMXV3SGVBWWM4SThxQlI1WFA1QVpFVFp6TC9NM0V6T3pCUFN6QUZmQzJ6T1d2ZkpsMnZmTGwyQnJtdUN4OWxVRlVCemFHelR6bHhCREhHU0hVVkpqOUszeXJrZ3NxT0dHWHBZTENPaHVMV1N0UnptU1N0VGhWT2JVVklhOFlEdTNjMFJwMUgxNlJvOXc5MFFFSTNlSVFvdmdJckNnNk0zbFpKbWxETkFuazdqTkE2cUsrWkhNcUIiOwoJInB1cmNoYXNlLWluZm8iID0gImV3b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGNITjBJaUE5SUNJeU1ESXpMVEE0TFRFd0lEQXhPalUwT2pNd0lFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW5CMWNtTm9ZWE5sTFdSaGRHVXRiWE1pSUQwZ0lqRTJPVEUyTlRjMk56QXdOVEVpT3dvSkluVnVhWEYxWlMxcFpHVnVkR2xtYVdWeUlpQTlJQ0l3TURBd09ERXhNQzB3TURFME5UVXhRekJETmtJNE1ERkZJanNLQ1NKdmNtbG5hVzVoYkMxMGNtRnVjMkZqZEdsdmJpMXBaQ0lnUFNBaU1qQXdNREF3TURNNE56TTJNRGd4TlNJN0Nna2lZblp5Y3lJZ1BTQWlNU0k3Q2draVlYQndMV2wwWlcwdGFXUWlJRDBnSWpZME5URXhPVEE0TWpRaU93b0pJblJ5WVc1ellXTjBhVzl1TFdsa0lpQTlJQ0l5TURBd01EQXdNemczTXpZd09ERTFJanNLQ1NKeGRXRnVkR2wwZVNJZ1BTQWlNU0k3Q2draWFXNHRZWEJ3TFc5M2JtVnljMmhwY0MxMGVYQmxJaUE5SUNKUVZWSkRTRUZUUlVRaU93b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGJYTWlJRDBnSWpFMk9URTJOVGMyTnpBd05URWlPd29KSW5WdWFYRjFaUzEyWlc1a2IzSXRhV1JsYm5ScFptbGxjaUlnUFNBaVJUQTVPRGN4TTBVdFFqUXlNeTAwUXpVekxUZzVSakF0TkRKRE5FSkJSVEl3UTBNMElqc0tDU0pwZEdWdExXbGtJaUE5SUNJMk5EVXhNVGt4TVRJNElqc0tDU0pwY3kxcGJpMXBiblJ5YnkxdlptWmxjaTF3WlhKcGIyUWlJRDBnSW1aaGJITmxJanNLQ1NKd2NtOWtkV04wTFdsa0lpQTlJQ0pqYjIwdWRHOXdhbTk1TG5wbGRYTmtaVzF2TG1saGNERWlPd29KSW5CMWNtTm9ZWE5sTFdSaGRHVWlJRDBnSWpJd01qTXRNRGd0TVRBZ01EZzZOVFE2TXpBZ1JYUmpMMGROVkNJN0Nna2lhWE10ZEhKcFlXd3RjR1Z5YVc5a0lpQTlJQ0ptWVd4elpTSTdDZ2tpYjNKcFoybHVZV3d0Y0hWeVkyaGhjMlV0WkdGMFpTSWdQU0FpTWpBeU15MHdPQzB4TUNBd09EbzFORG96TUNCRmRHTXZSMDFVSWpzS0NTSmlhV1FpSUQwZ0ltTnZiUzUwYjNCcWIza3VlbVYxYzJSbGJXOGlPd29KSW5CMWNtTm9ZWE5sTFdSaGRHVXRjSE4wSWlBOUlDSXlNREl6TFRBNExURXdJREF4T2pVME9qTXdJRUZ0WlhKcFkyRXZURzl6WDBGdVoyVnNaWE1pT3dwOSI7CgkiZW52aXJvbm1lbnQiID0gIlNhbmRib3giOwoJInBvZCIgPSAiMTAwIjsKCSJzaWduaW5nLXN0YXR1cyIgPSAiMCI7Cn0="

    def test_order_ios_verify(self):
        """[iosV1支付确认]已成功订单重复确认"""
        path = "/order/ios-verify"
        body = {
                "order_id": "i_20230810165355_d4gljK",
                "paper": self.paper,
                "pay_currency": "USD",
                "lang": "1",
                "pay_amount": "0.99",
                "platform": "ios",
                "sdk_version": "2.8.0",
                "appid": get_app_id()
            }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_order_ios_verify_with_blank_order_id(self):
        """[iosV1支付确认]orderId为空"""
        path = "/order/ios-verify"
        body = {
            "order_id": "",
            "paper": self.paper,
            "pay_currency": "USD",
            "lang": "1",
            "pay_amount": "0.99",
            "platform": "ios",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_with_blank_paper(self):
        """[iosV1支付确认]paper为空"""
        path = "/order/ios-verify"
        body = {
            "order_id": "i_20230810165355_d4gljK",
            "paper": "",
            "pay_currency": "USD",
            "lang": "1",
            "pay_amount": "0.99",
            "platform": "ios",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_with_empty_body(self):
        """[iosV1支付确认]参数校验：空表单"""
        path = "/order/ios-verify"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_with_blank_body(self):
        """[iosV1支付确认]参数校验：表单为空"""
        path = "/order/ios-verify"
        body = {
            "order_id": "",
            "paper": "",
            "pay_currency": "",
            "lang": "",
            "pay_amount": "",
            "platform": "",
            "sdk_version": "",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_with_null_body(self):
        """[iosV1支付确认]参数校验：表单为null"""
        path = "/order/ios-verify"
        body = {
            "order_id": None,
            "paper": None,
            "pay_currency": None,
            "lang": None,
            "pay_amount": None,
            "platform": None,
            "sdk_version": None,
            "appid": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_without_order_id(self):
        """[iosV1支付确认]参数缺失，缺少order_id"""
        path = "/order/ios-verify"
        body = {
            "paper": self.paper,
            "pay_currency": "USD",
            "lang": "1",
            "pay_amount": "0.99",
            "platform": "ios",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_order_ios_verify_without_paper(self):
        """[iosV1支付确认]参数缺失，缺少transaction_id"""
        path = "/order/ios-verify"
        body = {
            "order_id": "i_20230810165355_d4gljK",
            "pay_currency": "USD",
            "lang": "1",
            "pay_amount": "0.99",
            "platform": "ios",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


