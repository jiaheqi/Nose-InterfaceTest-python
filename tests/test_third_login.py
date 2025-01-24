from unittest import TestCase

import json
from tests.components.httpclient import sdk_http_client
from tests.components.fake import generate_mobile_info, generate_device_id, generate_union_id, get_app_id
from tests.components.utils import register_user, bind_third

"""
[用户管理]--三方登录：
参数校验：
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.参数缺失只传其中部分参数
4.账号不存在：token无效
5.账号类型不存在：传入type枚举不存在的值
正常/异常：
1.正常登录
2.多种三方登录方式登录：Facebook，Twitter，Line，Google，QQ，微信，SMS，appleId
TODO:Facebook,Line,微信
3.使用绑定过的三方账号登录
"""

"""
[初始化]--获取目前开启的第三方登录信息：
参数校验：
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.参数缺失只传其中部分参数
正常/异常：
1.正常请求
"""


class TestThirdLogin(TestCase):

    def test_third_login_with_empty_param(self):
        """[用户管理]--三方登录异常，空表单"""
        path = "/v2/user/third-login"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_third_login_with_blank_param(self):
        """[用户管理]--三方登录异常，参数为空"""
        path = "/v2/user/third-login"
        body = {
            "device": "",
            "mobile_info": "",
            "platform": "",
            "secret_token": "",
            "token": "",
            "type": "",
            "union_id": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_third_login_with_null_param(self):
        """[用户管理]--三方登录异常，参数为null"""
        path = "/v2/user/third-login"
        body = {
            "device": None,
            "mobile_info": None,
            "platform": None,
            "secret_token": None,
            "token": None,
            "type": None,
            "union_id": ""
        }
        response = sdk_http_client.post(path, body)
        # {'error_no': 1002, 'message': 'signature verification failure'}
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_third_login_with_part_param(self):
        """[用户管理]--三方登录异常，参数缺失：union_id不传"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "secret_token": "BnNVcrig8ZKVZuv9mqvYFez6EhbORfMTWyrN5tdqwLAOs",
            "token": "964475878611668992-xtZmGrWFOqjCwZNHfvOaooEeNDSMBcM",
            "type": "2"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1004)

    def test_third_login_invalid_token(self):
        """[用户管理]--三方登录异常，token无效"""
        # 目前未对token做校验
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "secret_token": "BnNVcrig8ZKVZuv9mqvYFez6EhbORfMTWyrN5tdqwLAOs",
            "token": "964475878611668992-xtZmGrWFOqjCwZNHfvOaooEeNDSMBcM-11111111",
            "type": "2",
            "union_id": generate_union_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_third_login_invalid_type(self):
        """[用户管理]--三方登录异常，type枚举不存在"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "secret_token": "BnNVcrig8ZKVZuv9mqvYFez6EhbORfMTWyrN5tdqwLAOs",
            "token": "964475878611668992-xtZmGrWFOqjCwZNHfvOaooEeNDSMBcM",
            "type": "100",
            "union_id": generate_union_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)

    def test_third_login(self):
        """[用户管理]--直接使用第三方登录，Twitter登录"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "secret_token": "BnNVcrig8ZKVZuv9mqvYFez6EhbORfMTWyrN5tdqwLAOs",
            "token": "964475878611668992-xtZmGrWFOqjCwZNHfvOaooEeNDSMBcM",
            "type": "2",
            "union_id": generate_union_id()
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_third_login_qq(self):
        """[用户管理]--直接使用第三方登录, QQ登录"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "android",
            "secret_token": "",
            "token": "6D4E4D8E7E3C714437126F79C069764C",
            "type": "8",
            "union_id": generate_union_id()
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_third_login_google(self):
        """[用户管理]--直接使用第三方登录,google登录"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "android",
            "secret_token": "",
            "token": "oKBXNRHRSJTeiMIHVYmOYpytXbVkaQzu",
            "type": "6",
            "union_id": generate_union_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_third_login_apple(self):
        """[用户管理]--直接使用第三方登录, appleId登录"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "secret_token": "",
            # token是重友的账号
            "token": "eyJraWQiOiJmaDZCczhDIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLnRvcGpveS56ZXVzZGVtbyIsImV4cCI6MTY5MTU3NjYyMCwiaWF0IjoxNjkxNDkwMjIwLCJzdWIiOiIwMDEzMzEuZjEyMGE4MzgxYjQ3NDU4NjhlMDdiZTA4MDY5YzFjZWEuMDYzOCIsImNfaGFzaCI6InN5ZUtYSUN0d0RrOGJCTlN6a3hIUnciLCJlbWFpbCI6IjI2Y3h3amI4NmNAcHJpdmF0ZXJlbGF5LmFwcGxlaWQuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiaXNfcHJpdmF0ZV9lbWFpbCI6InRydWUiLCJhdXRoX3RpbWUiOjE2OTE0OTAyMjAsIm5vbmNlX3N1cHBvcnRlZCI6dHJ1ZX0.Pw5rGpwbo6UhEdcFMpuPk_QqtR4mpzukXsjH3LFT55mDpcJPhlySAFWr5yxVJ5yH_OaAb9ZC1gV-_6qAADskzMSlwdjsWc9lTJoAhUq6SHySTRDZZ0Io5Cs-Gvs94DcuMCPmGfRf2owx9WHM-hSjrdwuVI4F3xtYEPtcfVNpM91SHoFLsonsavInMebIxxroXBPY2ZxECgaG2eTnqTZkOhgWVOaPkJowqVDRWYsmbqePz8a8ED5qCL8wFUGV4ZO_1BvtQldR7BK8ZZBJG-iY6GygqRDUXsTCRiGOU2c2EJDatU6WhqH2-eMwbE8-uJBZQHIaN-hzRo-poYYAIw2wYA",
            "type": "7",
            "union_id": generate_union_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_third_login_facebook(self):
        """[用户管理]--直接使用第三方登录, facebook登录"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "android",
            "secret_token": "",
            "token": "oKBXNRHRSJTeiMIHVYmOYpytXbVkaQzu",
            "type": "1",
            "union_id": generate_union_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_third_login_sms(self):
        """[用户管理]--直接使用第三方登录, sms登录"""
        path = "/v2/user/third-login"
        body = {
            "device": '7094433f6a4414ee',  # 验证码应该是和设备有关联，不可以随便填，否则会1004
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "android",
            "secret_token": "",
            "token": "1442",
            "type": "10",
            "union_id": "17600116844"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)

    def test_third_login_line(self):
        """[用户管理]--直接使用第三方登录, line登录"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "android",
            "secret_token": "",
            "token": "eyJhbGciOiJIUzI1NiJ9"
                     ".jPmSrxiHLcn244yGckFVoCcQ8WaDlGRFkeSHyry4jvYb6DWw_BL7Oq0gF0m2hRKu8g0zCODXD6SJfb9ghfijPFrvBnyZSUu6crEH0s4jmyefN5_7PJewQGMbY0Jl4rEPRvJSxM4thFbwb0x0BN_XBoQhVGoUEBdyoX0xOGxLqeY.kDauZeO4f2lGbzsUXR_lBgKfUCZdUpv4Mshgt7s4QOM",
            "type": "3",
            "union_id": generate_union_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)


class TestThirdLoginWithBindAccount(TestCase):
    def setUp(self):
        self.user_id = str(register_user().get("id"))
        self.union_id = generate_union_id()

        bind_third(self.user_id, self.union_id)

    def test_get_bind_list(self):
        """[用户管理]--使用绑定过的第三方账号登录"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "android",
            "secret_token": "",
            "token": "6D4E4D8E7E3C714437126F79C069764C",
            "type": "2",
            "union_id": self.union_id
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("id"), self.user_id)


class TestThirdLoginWithMultiAccount(TestCase):
    def setUp(self):
        self.user_id1 = str(register_user().get("id"))
        self.user_id2 = str(register_user().get("id"))
        self.union_id = generate_union_id()

        bind_third(self.user_id1, self.union_id)
        bind_third(self.user_id2, self.union_id)

    def test_get_bind_list(self):
        """[用户管理]--获取用户已经绑定的第三方账号信息, 绑定多个账号"""
        path = "/v2/user/third-login"
        body = {
            "device": generate_device_id(),
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "android",
            "secret_token": "",
            "token": "6D4E4D8E7E3C714437126F79C069764C",
            "type": "2",
            "union_id": self.union_id
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertIsInstance(response.json().get("result"), list)
        self.assertEqual(len(response.json().get("result")), 2)


class TestThirdList(TestCase):

    def test_user_third_list(self):
        """[初始化]--获取目前开启的第三方登录信息"""
        path = "user/third-list"
        body = {
            "appid": get_app_id(),
            "platform": "android", "sdk_version": "2.7.1", "user_id": "",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_user_third_list_with_empty_body(self):
        """[初始化]--获取目前开启的第三方登录信息，空表单"""
        path = "user/third-list"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_user_third_list_with_blank_body(self):
        """[初始化]--获取目前开启的第三方登录信息，参数为空"""
        path = "user/third-list"
        body = {
            "appid": "", "platform": "", "sdk_version": "", "user_id": "",
            "sign": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_third_list_with_null_body(self):
        """[初始化]--获取目前开启的第三方登录信息，参数为null"""
        path = "user/third-list"
        body = {
            "appid": None, "platform": None, "sdk_version": None, "user_id": None,
            "sign": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)
