from unittest import TestCase

from tests.components.httpclient import sdk_http_client
from tests.components.utils import register_user
from tests.components.fake import generate_device_id

"""
[用户管理]--上传用户信息
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失，只传部分参数
4.userId不存在（无校验）
正常/异常请求：
1.正常请求
"""


class TestRole(TestCase):

    def setUp(self) -> None:
        self.user_id = register_user().get("id")
        self.device = generate_device_id()

    def test_role_save(self):
        """[用户管理]--上传用户信息"""
        path = "/role/save"
        body = {
            "device": self.device,
            "platform": "ios",
            "level": "12",
            "server_name": "server_name",
            "server_id": "1111",
            "role_id": "1111",
            "user_id": str(self.user_id),
            "role_name": "role_name",
            "vip": "5"
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_role_save_with_empty_body(self):
        """[用户管理]--上传用户信息,空表单异常"""
        path = "/role/save"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_role_save_with_blank_body(self):
        """[用户管理]--上传用户信息,参数为空"""
        path = "/role/save"
        body = {
            "device": "",
            "platform": "",
            "level": "",
            "server_name": "",
            "server_id": "",
            "role_id": "",
            "user_id": "",
            "role_name": "",
            "vip": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_role_save_with_null_body(self):
        """[用户管理]--上传用户信息,参数为null"""
        path = "/role/save"
        body = {
            "device": None,
            "platform": None,
            "level": None,
            "server_name": None,
            "server_id": None,
            "role_id": None,
            "user_id": None,
            "role_name": None,
            "vip": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_role_save_with_invalid_userId(self):
        """[用户管理]--上传用户信息,用户不存在"""
        path = "/role/save"
        body = {
            "device": self.device,
            "platform": "ios",
            "level": "12",
            "server_name": "server_name",
            "server_id": "1111",
            "role_id": "1111",
            "user_id": "000",
            "role_name": "role_name",
            "vip": "5"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
