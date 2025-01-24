from unittest import TestCase

import json
from tests.components.httpclient import sdk_http_client
from tests.components.fake import generate_mobile_info, generate_device_id, generate_union_id
from tests.components.utils import register_user

"""
[用户管理]--用户登录：
参数校验
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.参数缺失只传其中部分参数：用户为空；设备号为空
4.设备号变更
5.用户不存在
正常/异常
1.正常登录+返回值校验
"""


class TestLogin(TestCase):
    def setUp(self) -> None:
        self.device = generate_device_id()
        user = register_user(self.device)
        self.account = user.get("account")

    def test_user_login_with_empty_body(self):
        """[用户管理]--用户登录, 空表单异常"""
        path = "/user/login"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_login_with_blank_body(self):
        """[用户管理]--用户登录, 参数值为空"""
        path = "/user/login"
        body = {
            "account": "",
            "device": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_login_with_null_body(self):
        """[用户管理]--用户登录, 参数值为null"""
        path = "/user/login"
        body = {
            "account": None,
            "device": None
        }
        response = sdk_http_client.post(path, body)
        # {'error_no': 1002, 'message': 'signature verification failure'}
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_user_login_with_part_body_account(self):
        """[用户管理]--用户登录, 设备号不传"""
        path = "/user/login"
        body = {
            "account": self.account
        }
        response = sdk_http_client.post(path, body)
        # {'error_no': 1003, 'message': "Key: 'Login.device' Error:Field validation for 'device' failed on the
        # 'required' tag"}
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_login_with_part_body_device(self):
        """[用户管理]--用户登录, 用户不传"""
        path = "/user/login"
        body = {
            "device": self.device
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1006)

    def test_user_login(self):
        """[用户管理]--用户登录:正常登录+返回值校验"""
        path = "/user/login"
        body = {
            "account": self.account,
            # "account":"958162217",
            "device": self.device
        }
        print(sdk_http_client.host)
        print(sdk_http_client.headers)
        response = sdk_http_client.post(path, body)
        print(response.json())
        dict_response = response.json()
        self.assertIn("error_no", dict_response)
        self.assertIn("message", dict_response)
        self.assertIn("result", dict_response)
        result = dict_response['result']
        self.assertIn("id", result)
        self.assertIn("account", result)
        self.assertIn("token", result)
        self.assertIn("is_real_name_authentication", result)
        self.assertIn("adult", result)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_user_login_invalid_device_id(self):
        """[用户管理]--用户登录, 设备变更"""
        path = "/user/login"
        body = {
            "account": self.account,
            "device": generate_device_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)

    def test_user_login_invalid_device_id(self):
        """[用户管理]--用户登录, 用户不存在"""
        path = "/user/login"
        body = {
            "account": "123",
            "device": generate_device_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1006)
