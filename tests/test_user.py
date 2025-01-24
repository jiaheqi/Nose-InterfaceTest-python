import json
from unittest import TestCase
from tests.components.fake import generate_mobile_info, generate_device_id
from tests.components.httpclient import sdk_http_client, server_http_client, another_sdk_http_client
from tests.components.utils import register_user, user_login

PATH = "/user/bind-third"
"""
[用户管理]--用户注册：
参数校验
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.参数缺失只传其中部分参数：手机信息为空；设备号为空；平台为空
4.不合法的设备号信息
5.使用不存在的force_renew枚举
正常/异常
1.正常请求+返回值校验
2.使用设备ID获取之前的用户信息
3.使用设备ID强制生成新账号
"""
"""
[用户管理]--用户注销：
参数校验
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
正常/异常
1.正常请求
"""
"""
[用户管理]--用户更新：
参数校验
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.参数缺失只传其中部分参数：缺少user_id，缺少name
4.user_id不存在
正常/异常
1.正常请求
"""


class TestUserRegister(TestCase):

    def test_user_register(self):
        """[用户管理]--用户注册, 正常请求"""
        path = "/user/register"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertNotEqual(response.json().get("id"), 0)
        self.assertNotEqual(response.json().get("account"), 0)

    def test_user_register_with_diff_appid_same_device(self):
        """[用户管理]--用户注册，绑定设备注册，同一个设备不同appid返回不同account
            且登录确认可以成功
        """
        path = "/user/register"
        device_id = generate_device_id()
        mobile_info = json.dumps(generate_mobile_info())
        body = {
            "device": device_id,
            "mobile_info": mobile_info,
            "platform": "Android",
            "force_renew": "false"
        }
        response = sdk_http_client.post(path, body)
        account = response.json().get("result").get("account")
        user_id = response.json().get("result").get("id")
        login_info = user_login(account, device_id)
        token = login_info.get("token")
        path_login_verify = "/login/verify"
        body1 = {
            "user_id": str(user_id),
            "token": token
        }
        res_login_verify1 = server_http_client.post(path_login_verify, body1)
        response1 = another_sdk_http_client.post(path, body)
        account1 = response1.json().get("result").get("account")
        user_id1 = response.json().get("result").get("id")
        login_info1 = user_login(account, device_id)
        token1 = login_info1.get("token")
        body2 = {
            "user_id": str(user_id1),
            "token": token1
        }
        res_login_verify2 = server_http_client.post(path_login_verify, body2)
        self.assertNotEqual(account, account1)
        self.assertEqual(res_login_verify1.json().get("error_no"), 0)
        self.assertEqual(res_login_verify2.json().get("error_no"), 0)

    def test_user_register_with_empty_body(self):
        """[用户管理]--用户注册, 空表单"""
        path = "/user/register"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_register_with_blank_body(self):
        """[用户管理]--用户注册, 参数为空"""
        path = "/user/register"
        body = {
            "device": "",
            "mobile_info": "",
            "platform": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_register_with_null_body(self):
        """[用户管理]--用户注册, 参数为null"""
        path = "/user/register"
        body = {
            "device": None,
            "mobile_info": None,
            "platform": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_user_register_without_mobileInfo(self):
        """[用户管理]--用户注册, 缺少手机信息"""
        path = "/user/register"
        body = {
            "device": generate_device_id(),
            "platform": "ios"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_user_register_without_device(self):
        """[用户管理]--用户注册, 缺少设备ID"""
        path = "/user/register"
        body = {
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
        }

        response = sdk_http_client.post(path, body)
        self.assertNotEqual(response.json().get("error_no"), 0)

    def test_user_register_without_platform(self):
        """[用户管理]--用户注册, 缺少平台信息"""
        path = "/user/register"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
        }

        response = sdk_http_client.post(path, body)
        self.assertNotEqual(response.json().get("error_no"), 0)

    def test_user_register_with_invalid_mobile_info(self):
        """[用户管理]--用户注册, 不合法的设备信息"""
        path = "/user/register"
        body = {
            "device": "123",
            "platform": "ios",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_user_register_with_exist_device_id(self):
        """[用户管理]--用户注册, 使用设备ID获取之前的账号"""
        path = "/user/register"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "force_renew": "false"
        }

        resp1 = sdk_http_client.post(path, body)
        resp2 = sdk_http_client.post(path, body)
        self.assertEqual(resp1.json().get("error_no"), 0)
        self.assertEqual(resp1.json().get("error_no"), 0)
        self.assertEqual(resp1.json().get("result", {}).get("account"), resp2.json().get("result", {}).get("account"))

    def test_user_register_force_renew(self):
        """[用户管理]--用户注册, 使用相同的设备ID强制生成新账号"""
        path = "/user/register"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "force_renew": "true"
        }

        resp1 = sdk_http_client.post(path, body)
        resp2 = sdk_http_client.post(path, body)
        self.assertEqual(resp1.json().get("error_no"), 0)
        self.assertEqual(resp1.json().get("error_no"), 0)
        self.assertNotEqual(resp1.json().get("result", {}).get("account"),
                            resp2.json().get("result", {}).get("account"))

    def test_user_register_with_invalid_force_renew(self):
        """[用户管理]--用户注册, 使用不存在的force_renew枚举"""
        path = "/user/register"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "force_renew": "123"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)


class TestUserUnRegister(TestCase):

    def test_user_unregister_with_empty_body(self):
        """[用户管理]--用户注销, 空表单"""
        path = "/user/unregister"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_unregister_with_blank_body(self):
        """[用户管理]--用户注销, 参数为空"""
        path = "/user/unregister"
        body = {
            "user_id": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_unregister_with_null_body(self):
        """[用户管理]--用户注销,参数为null"""
        path = "/user/unregister"
        body = {
            "user_id": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)


class TestUserInfo(TestCase):
    def test_get_user_info_with_empty_body(self):
        """[用户管理]--请求用户信息，表单为空的异常"""

        path = "/user/info"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertNotEqual(response.json().get("error_no"), 0)

    def test_get_user_info_not_exists(self):
        """[用户管理]--请求用户信息，用户不存在"""
        path = "/user/info"
        body = {
            "user_id": "123"
        }
        response = sdk_http_client.post(path, body)
        self.assertNotEqual(response.json().get("error_no"), 0)


class TestUserUpdate(TestCase):
    def setUp(self) -> None:
        self.user_id = register_user().get("id")

    def test_user_update(self):
        """[用户管理]--更新用户信息"""
        path = "/user/update"
        body = {
            "user_id": str(self.user_id),
            "name": "new_name"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_user_update_with_empty_body(self):
        """[用户管理]--更新用户信息,空表单"""
        path = "/user/update"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_update_with_blank_body(self):
        """[用户管理]--更新用户信息,参数为空"""
        path = "/user/update"
        body = {
            "user_id": "",
            "name": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_update_with_null_body(self):
        """[用户管理]--更新用户信息,参数为null"""
        path = "/user/update"
        body = {
            "user_id": None,
            "name": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_user_update_without_name(self):
        """[用户管理]--更新用户信息,参数缺失，缺少name"""
        path = "/user/update"
        body = {
            "user_id": str(self.user_id)
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_user_update_without_user_id(self):
        """[用户管理]--更新用户信息,参数缺失，缺少name"""
        path = "/user/update"
        body = {
            "name": "new_name"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_update_with_invalid_user_id(self):
        """[用户管理]--更新用户信息,user_id不存在"""
        path = "/user/update"
        body = {
            "user_id": "000",
            "name": "new_name"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 10017)


class TestUserThirdList(TestCase):

    def test_user_third_list(self):
        """[用户管理]--获取用户可以绑定的第三方平台列表"""
        path = "/user/third-list"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
