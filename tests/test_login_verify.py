from unittest import TestCase

import json
from tests.components.httpclient import server_http_client
from tests.components.fake import generate_device_id
from tests.components.utils import register_user, user_login

"""
[用户管理]--用户登录验证
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失，只传部分参数
4.userid不存在
5.token无效
正常/异常：
1.正常验证+返回值校验
"""


class TestLoginVerify(TestCase):
    def setUp(self) -> None:
        device = generate_device_id()
        user = register_user(device)
        self.account = user.get("account")
        self.login_info = user_login(self.account, device)

    def test_user_login_verify_token(self):
        """[用户管理]--用户登录验证, 服务端验证Token"""

        user_id = self.login_info.get("id")
        token = self.login_info.get("token")
        path = "/login/verify"
        body = {
            "user_id": str(user_id),
            "token": token
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("account"), self.account)
        self.assertEqual(response.json().get("result").get("user_id"), user_id)

    def test_user_login_verify_token_with_empty_body(self):
        """[用户管理]--用户登录验证，空表单"""
        path = "/login/verify"
        body = {
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1001)

    def test_user_login_verify_token_with_blank_body(self):
        """[用户管理]--用户登录验证，参数为空"""
        path = "/login/verify"
        body = {
            "user_id": "",
            "token": ""
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1001)

    def test_user_login_verify_token_with_null_body(self):
        """[用户管理]--用户登录验证，参数为null"""
        path = "/login/verify"
        body = {
            "user_id": None,
            "token": None
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1001)

    def test_user_login_verify_token_with_part_body_user_id(self):
        """[用户管理]--用户登录验证，参数缺失：只传userid"""
        path = "/login/verify"
        user_id = self.login_info.get("id")
        body = {
            "user_id": str(user_id)
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1001)

    def test_user_login_verify_token_with_part_body_token(self):
        """[用户管理]--用户登录验证，参数缺失：只传token"""
        path = "/login/verify"
        token = self.login_info.get("token")
        body = {
            "token": token
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1001)

    def test_user_login_verify_token_with_invalid_user_id(self):
        """[用户管理]--用户登录验证，userid不存在"""
        path = "/login/verify"
        token = self.login_info.get("token")
        body = {
            "user_id": "123",
            "token": token
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 10017)

    def test_user_login_verify_token_with_invalid_token(self):
        """[用户管理]--用户登录验证，token无效"""
        path = "/login/verify"
        user_id = self.login_info.get("id")
        body = {
            "user_id": str(user_id),
            "token": "111"
        }
        response = server_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 10002)
