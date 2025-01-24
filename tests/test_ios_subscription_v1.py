from unittest import TestCase

from tests.components.fake import generate_device_id, get_app_id
from tests.components.httpclient import sdk_http_client
from tests.components.tools import time_format_timestamp_ms
from tests.components.utils import role_save, register_user

"""
[iosV1订阅]创建ios订阅订单
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失：缺少userId，roleId，productId，price
4.金额不合法：汉字，字母，符号
5.金额小数位数不合法
6.金额为0
正常/异常：
1.正常请求
"""

"""
[iosV1订阅确认]ios订单确认
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


class TestIosSubscriptionExchange(TestCase):
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

    def test_ios_subscription_exchange(self):
        """[ios订阅]创建订单，正常请求"""
        path = "/subscription/ios-exchange"
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
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)
        self.assertIsNotNone(response.json().get('result').get('order_id'))

    def test_ios_subscription_exchange_with_empty_body(self):
        """[ios订阅]创建订单，空白单"""
        path = "/subscription/ios-exchange"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_blank_body(self):
        """[ios订阅]创建订单，参数为空"""
        path = "/subscription/ios-exchange"
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
            "lang": "",
            "extend": "",
            "device": "",
            "role_id": "",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_null_body(self):
        """[ios订阅]创建订单，参数为null"""
        path = "/subscription/ios-exchange"
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
            "lang": None,
            "extend": None,
            "device": None,
            "role_id": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_without_user_id(self):
        """[ios订阅]创建订单，参数缺失，缺少user_id"""
        path = "/subscription/ios-exchange"
        body = {
            "appid": get_app_id(),
            "vip": "5",
            "server_name": "玩家区服",
            "server_id": "1",
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "price": "0.99",
            "platform": "ios",
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_without_role_id(self):
        """[ios订阅]创建订单，参数缺失，缺少role_id"""
        path = "/subscription/ios-exchange"
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
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_without_role_name(self):
        """[ios订阅]创建订单，参数缺失，缺少role_name"""
        path = "/subscription/ios-exchange"
        body = {
            "appid": get_app_id(),
            "vip": "5",
            "server_name": "玩家区服",
            "server_id": "1",
            "user_id": self.user_id,
            "sdk_version": "2.8.0",
            "price": "0.99",
            "platform": "ios",
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_without_price(self):
        """[ios订阅]创建订单，参数缺失，缺少price"""
        path = "/subscription/ios-exchange"
        body = {
            "appid": get_app_id(),
            "vip": "5",
            "server_name": "玩家区服",
            "server_id": "1",
            "user_id": self.user_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "platform": "ios",
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_invalid_price(self):
        """[ios订阅]创建订单，参数不合法，金额为汉字"""
        path = "/subscription/ios-exchange"
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
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_invalid_price1(self):
        """[ios订阅]创建订单，参数不合法，金额为字母"""
        path = "/subscription/ios-exchange"
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
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_invalid_price2(self):
        """[ios订阅]创建订单，参数不合法，金额为符号"""
        path = "/subscription/ios-exchange"
        body = {
            "appid": get_app_id(),
            "vip": "5",
            "server_name": "玩家区服",
            "server_id": "1",
            "user_id": self.user_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "price": "!@#  ",
            "platform": "ios",
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_invalid_price3(self):
        """[ios订阅]创建订单，参数不合法，金额为小数位数不合法"""
        path = "/subscription/ios-exchange"
        body = {
            "appid": get_app_id(),
            "vip": "5",
            "server_name": "玩家区服",
            "server_id": "1",
            "user_id": self.user_id,
            "role_name": self.role_name,
            "sdk_version": "2.8.0",
            "price": "0.00099999",
            "platform": "ios",
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 0)

    def test_ios_subscription_exchange_with_invalid_price(self):
        """[ios订阅]创建订单，参数不合法，金额为0"""
        path = "/subscription/ios-exchange"
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
            "product_id": "com.topjoy.zeusdemo.sub1",
            "level": "12",
            "lang": "1",
            "extend": "serverId=3|userId=1011s3p60896|productId=121691658665",
            "device": self.device,
            "role_id": self.role_id,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


class TestIosSubscriptionVerify(TestCase):
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
        paper = "ewoJInNpZ25hdHVyZSIgPSAiQkt5L2prSS9lWU9UbzE3Q000N0JhN3l6d2tlcTViUHRUdTZDZW83d1I5YXNuaENCMDRSRWkya0tPOXdiS3FtaTJpTVZBY1c1UmU4OGVJSFF4VllHZ2MzcmtRMGM5aXZMcUNYeHlpTGZSRGJMbU84TFdoM3NJRm1POHZEM0UvT3V2cmdqUWVvY3hObmhZb01naW5qZmVrN2FuTEw2dTBYdVVTd25xRFhpMGUrRGZtVWpWMy9OU1hhRjVKTGFVck5IWVJVWkFQTmhKbDFtVzZwRjI4N3I1UlJNa3lJVEJjbCtJeXlkRmUrbFlscitYaWlmZTB5Qk8wQzBvNFdPY29GN2tLWnRVNnkzeDNjamJPOEx1TS9DMHIvTHUxQ2ZoN3d5aDZjNURHYmwwZkxUWTFmbW9vKzU1RVBSVVRIWmthMkpIdlZiaU14SzJVbmFxR1R4Wko4ZmxoRUFBQVhLTUlJRnhqQ0NCSzZnQXdJQkFnSVFGZWVmemxKVkNtVUJmSkhmNU82eldUQU5CZ2txaGtpRzl3MEJBUXNGQURCMU1VUXdRZ1lEVlFRREREdEJjSEJzWlNCWGIzSnNaSGRwWkdVZ1JHVjJaV3h2Y0dWeUlGSmxiR0YwYVc5dWN5QkRaWEowYVdacFkyRjBhVzl1SUVGMWRHaHZjbWwwZVRFTE1Ba0dBMVVFQ3d3Q1J6VXhFekFSQmdOVkJBb01Da0Z3Y0d4bElFbHVZeTR4Q3pBSkJnTlZCQVlUQWxWVE1CNFhEVEl5TURrd01qRTVNVE0xTjFvWERUSTBNVEF3TVRFNU1UTTFObG93Z1lreE56QTFCZ05WQkFNTUxrMWhZeUJCY0hBZ1UzUnZjbVVnWVc1a0lHbFVkVzVsY3lCVGRHOXlaU0JTWldObGFYQjBJRk5wWjI1cGJtY3hMREFxQmdOVkJBc01JMEZ3Y0d4bElGZHZjbXhrZDJsa1pTQkVaWFpsYkc5d1pYSWdVbVZzWVhScGIyNXpNUk13RVFZRFZRUUtEQXBCY0hCc1pTQkpibU11TVFzd0NRWURWUVFHRXdKVlV6Q0NBU0l3RFFZSktvWklodmNOQVFFQkJRQURnZ0VQQURDQ0FRb0NnZ0VCQUx4RXpndXRhakIycjhBSkREUjZHV0h2dlNBTjlmcERuaFAxclBNOGt3N1haWnQwd2xvM0oxVHdqczFHT29MTWRiOFM0QXNwN2xocm9PZENLdmVIQUoraXpLa2k1bTNvRGVmTEQvVFFaRnV6djQxanpjS2JZckFwMTk3QW80MnRHNlQ0NjJqYmM0WXVYOHk3SVgxcnVEaHVxKzhpZzBnVDlrU2lwRWFjNVdMc2REdC9ONVNpZG1xSUlYc0VmS0hUczU3aU5XMm5qbyt3NDJYV3lETWZUbzZLQSt6cHZjd2Z0YWVHamdUd2tPKzZJWTV0a21KeXdZblFtUDdqVmNsV3hqUjAvdlFlbWtOd1lYMStoc0o1M1ZCMTNRaXc1S2kxZWpaOWwvejVTU0FkNXhKaXFHWGFQQlpZL2laUmo1RjVxejFidS9rdTB6dFNCeGd3NTM4UG1POENBd0VBQWFPQ0Fqc3dnZ0kzTUF3R0ExVWRFd0VCL3dRQ01BQXdId1lEVlIwakJCZ3dGb0FVR1l1WGpVcGJZWGhYOUtWY05SS0tPUWpqc0hVd2NBWUlLd1lCQlFVSEFRRUVaREJpTUMwR0NDc0dBUVVGQnpBQ2hpRm9kSFJ3T2k4dlkyVnlkSE11WVhCd2JHVXVZMjl0TDNkM1pISm5OUzVrWlhJd01RWUlLd1lCQlFVSE1BR0dKV2gwZEhBNkx5OXZZM053TG1Gd2NHeGxMbU52YlM5dlkzTndNRE10ZDNka2NtYzFNRFV3Z2dFZkJnTlZIU0FFZ2dFV01JSUJFakNDQVE0R0NpcUdTSWIzWTJRRkJnRXdnZjh3TndZSUt3WUJCUVVIQWdFV0syaDBkSEJ6T2k4dmQzZDNMbUZ3Y0d4bExtTnZiUzlqWlhKMGFXWnBZMkYwWldGMWRHaHZjbWwwZVM4d2djTUdDQ3NHQVFVRkJ3SUNNSUcyRElHelVtVnNhV0Z1WTJVZ2IyNGdkR2hwY3lCalpYSjBhV1pwWTJGMFpTQmllU0JoYm5rZ2NHRnlkSGtnWVhOemRXMWxjeUJoWTJObGNIUmhibU5sSUc5bUlIUm9aU0IwYUdWdUlHRndjR3hwWTJGaWJHVWdjM1JoYm1SaGNtUWdkR1Z5YlhNZ1lXNWtJR052Ym1ScGRHbHZibk1nYjJZZ2RYTmxMQ0JqWlhKMGFXWnBZMkYwWlNCd2IyeHBZM2tnWVc1a0lHTmxjblJwWm1sallYUnBiMjRnY0hKaFkzUnBZMlVnYzNSaGRHVnRaVzUwY3k0d01BWURWUjBmQkNrd0p6QWxvQ09nSVlZZmFIUjBjRG92TDJOeWJDNWhjSEJzWlM1amIyMHZkM2RrY21jMUxtTnliREFkQmdOVkhRNEVGZ1FVSXNrOGUyTVRoYjQ2TzhVenFiVDZzYkNDa3hjd0RnWURWUjBQQVFIL0JBUURBZ2VBTUJBR0NpcUdTSWIzWTJRR0N3RUVBZ1VBTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElCQVFBOFJ1N1BxRHk0L1o2RHkxSHc5cWhSL09JSEhZSWszTzZTaWh2cVRhanFPMCtITXBvNU9kdGIrRnZhVFkzTit3bEtDN0hObWhsdlRzZjlhRnM3M1BsWGo1TWtTb1IwamFBa1ozYzVnamtOank5OGdZRVA3ZXRiK0hXMC9QUGVsSkc5VElVY2ZkR09aMlJJZ2dZS3NHRWt4UEJRSzFaYXJzMXV3SGVBWWM4SThxQlI1WFA1QVpFVFp6TC9NM0V6T3pCUFN6QUZmQzJ6T1d2ZkpsMnZmTGwyQnJtdUN4OWxVRlVCemFHelR6bHhCREhHU0hVVkpqOUszeXJrZ3NxT0dHWHBZTENPaHVMV1N0UnptU1N0VGhWT2JVVklhOFlEdTNjMFJwMUgxNlJvOXc5MFFFSTNlSVFvdmdJckNnNk0zbFpKbWxETkFuazdqTkE2cUsrWkhNcUIiOwoJInB1cmNoYXNlLWluZm8iID0gImV3b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGNITjBJaUE5SUNJeU1ESXpMVEE0TFRFMElEQXlPakU0T2pFM0lFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW5GMVlXNTBhWFI1SWlBOUlDSXhJanNLQ1NKemRXSnpZM0pwY0hScGIyNHRaM0p2ZFhBdGFXUmxiblJwWm1sbGNpSWdQU0FpTWpFek56STFPVFlpT3dvSkluVnVhWEYxWlMxMlpXNWtiM0l0YVdSbGJuUnBabWxsY2lJZ1BTQWlSREUxT0VNNE5FTXROemd5UmkwMFJVRXdMVUl6TUVNdE1qUTVORVF3UmpKQlJrSkJJanNLQ1NKdmNtbG5hVzVoYkMxd2RYSmphR0Z6WlMxa1lYUmxMVzF6SWlBOUlDSXhOamt5TURBME5qazNNREF3SWpzS0NTSmxlSEJwY21WekxXUmhkR1V0Wm05eWJXRjBkR1ZrSWlBOUlDSXlNREl6TFRBNExURTBJREE1T2pNek9qRXdJRVYwWXk5SFRWUWlPd29KSW1sekxXbHVMV2x1ZEhKdkxXOW1abVZ5TFhCbGNtbHZaQ0lnUFNBaVptRnNjMlVpT3dvSkluQjFjbU5vWVhObExXUmhkR1V0YlhNaUlEMGdJakUyT1RJd01EVTBNVEF3TURBaU93b0pJbVY0Y0dseVpYTXRaR0YwWlMxbWIzSnRZWFIwWldRdGNITjBJaUE5SUNJeU1ESXpMVEE0TFRFMElEQXlPak16T2pFd0lFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW1sekxYUnlhV0ZzTFhCbGNtbHZaQ0lnUFNBaVptRnNjMlVpT3dvSkltbDBaVzB0YVdRaUlEMGdJalkwTmpFek9ETTRPRGtpT3dvSkluVnVhWEYxWlMxcFpHVnVkR2xtYVdWeUlpQTlJQ0l3TURBd09ERXhNQzB3TURFME5UVXhRekJETmtJNE1ERkZJanNLQ1NKdmNtbG5hVzVoYkMxMGNtRnVjMkZqZEdsdmJpMXBaQ0lnUFNBaU1qQXdNREF3TURNNE9UWXlNemN5TnlJN0Nna2laWGh3YVhKbGN5MWtZWFJsSWlBOUlDSXhOamt5TURBMU5Ua3dNREF3SWpzS0NTSmhjSEF0YVhSbGJTMXBaQ0lnUFNBaU5qUTFNVEU1TURneU5DSTdDZ2tpZEhKaGJuTmhZM1JwYjI0dGFXUWlJRDBnSWpJd01EQXdNREF6T1RReE9ETTRNemNpT3dvSkltbHVMV0Z3Y0MxdmQyNWxjbk5vYVhBdGRIbHdaU0lnUFNBaVVGVlNRMGhCVTBWRUlqc0tDU0ppZG5KeklpQTlJQ0l4SWpzS0NTSjNaV0l0YjNKa1pYSXRiR2x1WlMxcGRHVnRMV2xrSWlBOUlDSXlNREF3TURBd01ETTBNVGN5T0RNeklqc0tDU0ppYVdRaUlEMGdJbU52YlM1MGIzQnFiM2t1ZW1WMWMyUmxiVzhpT3dvSkluQnliMlIxWTNRdGFXUWlJRDBnSW1OdmJTNTBiM0JxYjNrdWVtVjFjMlJsYlc4dWMzVmlJanNLQ1NKd2RYSmphR0Z6WlMxa1lYUmxJaUE5SUNJeU1ESXpMVEE0TFRFMElEQTVPak13T2pFd0lFVjBZeTlIVFZRaU93b0pJbkIxY21Ob1lYTmxMV1JoZEdVdGNITjBJaUE5SUNJeU1ESXpMVEE0TFRFMElEQXlPak13T2pFd0lFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW05eWFXZHBibUZzTFhCMWNtTm9ZWE5sTFdSaGRHVWlJRDBnSWpJd01qTXRNRGd0TVRRZ01EazZNVGc2TVRjZ1JYUmpMMGROVkNJN0NuMD0iOwoJImVudmlyb25tZW50IiA9ICJTYW5kYm94IjsKCSJwb2QiID0gIjEwMCI7Cgkic2lnbmluZy1zdGF0dXMiID0gIjAiOwp9",
        self.order_id = "is_20230821105318_qk3gNx"
        self.paper = "".join(paper)
        role_save(device, self.user_id, self.role_id, self.role_name)

    def test_ios_subscription_verify(self):
        """[ios订阅确认]已确认订阅重复确认"""
        path = "/subscription/ios-verify"
        body = {
            "order_id": self.order_id,
            "paper": self.paper,
            "pay_currency": "USD",
            "lang": "1",
            "pay_amount": "0.99",
            "platform": "ios",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 10009)

    def test_ios_subscription_exchange_with_empty_body(self):
        """[ios订阅确认]空表单"""
        path = "/subscription/ios-verify"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_blank_body(self):
        """[ios订阅确认]参数为空"""
        path = "/subscription/ios-verify"
        body = {
            "order_id": "",
            "paper": "",
            "pay_currency": "",
            "lang": "",
            "pay_amount": "",
            "platform": "",
            "sdk_version": "",
            "appid": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_ios_subscription_exchange_with_null_body(self):
        """[ios订阅确认]参数为null"""
        path = "/subscription/ios-verify"
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

    def test_ios_subscription_exchange_without_paper(self):
        """[ios订阅确认]参数缺失，缺少paper"""
        path = "/subscription/ios-verify"
        body = {
            "order_id": self.order_id,
            "pay_currency": "USD",
            "lang": "1",
            "pay_amount": "0.99",
            "platform": "ios",
            "sdk_version": "2.8.0",
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)