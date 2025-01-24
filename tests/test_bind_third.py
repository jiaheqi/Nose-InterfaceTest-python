import json
from unittest import TestCase

from tests.components.httpclient import sdk_http_client
from tests.components.fake import generate_union_id
from tests.components.utils import register_user, bind_third

"""
[用户管理]--绑定第三方账号
参数校验：
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.参数缺失只传其中部分参数
4.用户ID不存在
5.union_id不存在
6.传入不存在的type枚举值
正常/异常：
1.正常绑定
2.多种三方账号绑定：Facebook，Twitter，Line，Google，QQ，微信，SMS
3.使用绑定过的三方账号重复绑定
4.绑定多个三方账号
5.绑定三方账号超过上限：3
"""
"""
[用户管理]--解绑第三方账号
参数校验：
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.参数缺失只传其中部分参数
4.用户ID不存在，用户ID没有绑定过
5.union_id不存在，union_id没有绑定过
6.传入type不存在的枚举值
正常/异常：
1.正常解绑
2.多种三方账号解绑：Facebook，Twitter，Line，Google，QQ，微信，SMS
3.已经解绑的账号重复解绑
"""
"""
[用户管理]--获取用户已经绑定的第三方账号信息
参数校验：
1.空表单，参数全不传
2.表单不为空，参数内容为空或null
3.用户ID不存在
正常/异常：
1.正常查询
"""


class TestBind(TestCase):
    def setUp(self):
        self.user_id = str(register_user().get("id"))
        self.union_id = generate_union_id()

    def test_bind_twitter_with_empty_body(self):
        """[用户管理]--绑定第三方账号,空表单"""
        path = "/user/bind-third"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_bind_twitter_with_part_body_userid(self):
        """[用户管理]--绑定第三方账号,参数缺失：只传userid"""
        path = "/user/bind-third"
        body = {
            "user_id": self.user_id
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_bind_twitter_with_part_body_unionid(self):
        """[用户管理]--绑定第三方账号,参数缺失：只传unionid"""
        path = "/user/bind-third"
        body = {
            "union_id": self.union_id
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_bind_twitter_without_type(self):
        """[用户管理]--绑定第三方账号,参数缺失：不传类型"""
        path = "/user/bind-third"
        body = {
            "union_id": self.union_id,
            "user_id": self.user_id
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_bind_twitter_with_null_body(self):
        """[用户管理]--绑定第三方账号,参数为null"""
        path = "/user/bind-third"
        body = {
            "type": None,
            "union_id": None,
            "user_id": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_bind_twitter_with_blank_body(self):
        """[用户管理]--绑定第三方账号,参数为空"""
        path = "/user/bind-third"
        body = {
            "type": "",
            "union_id": "",
            "user_id": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_bind_twitter(self):
        """[用户管理]--绑定第三方账号"""
        path = "/user/bind-third"
        body = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": self.user_id
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_bind_with_invalid_user_id(self):
        """[用户管理]--绑定第三方账号, 不存在的用户ID"""
        path = "/user/bind-third"
        body = {
            "type": "2",
            "union_id": "fake_union_id",
            "user_id": "123"
        }
        response = sdk_http_client.post(path, body)
        self.assertNotEqual(response.json().get("error_no"), 0)

    def test_bind_with_invalid_union_id(self):
        # 服务端的处理方式是如果unionID不存在绑定，会新建一条绑定记录
        # 理论上不存在这种情况
        """[用户管理]--绑定第三方账号, 不存在的unoinID"""
        path = "/user/bind-third"
        body = {
            "type": "2",
            "union_id": "fake_union_id",
            "user_id": self.user_id
        }
        response = sdk_http_client.post(path, body)
        self.assertNotEqual(response.json().get("error_no"), 0)

    def test_bind_with_invalid_type(self):
        """[用户管理]--绑定第三方账号, 不存在的type"""
        path = "/user/bind-third"
        body = {
            "type": "2000",
            "union_id": self.union_id,
            "user_id": self.user_id
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)


class TestDuplicateBind(TestCase):
    def setUp(self):
        self.user_id = str(register_user().get("id"))
        self.union_id = generate_union_id()

    def test_duplicate_bind_twitter(self):
        """[用户管理]--绑定第三方账号, 重复绑定报错"""
        path = "/user/bind-third"
        body = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": self.user_id
        }

        resp1 = sdk_http_client.post(path, body)
        self.assertEqual(resp1.json().get("error_no"), 0)
        resp2 = sdk_http_client.post(path, body)
        self.assertNotEqual(resp2.json().get("error_no"), 0)


class TestBindMultiAccount(TestCase):
    def setUp(self):
        self.user_id1 = str(register_user().get("id"))
        self.user_id2 = str(register_user().get("id"))
        self.user_id3 = str(register_user().get("id"))
        self.union_id = generate_union_id()

    def test_bind_multi_account(self):
        """[用户管理]--绑定第三方账号, 绑定多个账号"""
        path = "/user/bind-third"
        body1 = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": self.user_id1
        }

        resp1 = sdk_http_client.post(path, body1)
        self.assertEqual(resp1.json().get("error_no"), 0)

        body2 = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": self.user_id2
        }
        resp2 = sdk_http_client.post(path, body2)
        self.assertEqual(resp2.json().get("error_no"), 0)


class TestBindMultiAccountOverMax(TestCase):
    def setUp(self):
        self.user_id1 = str(register_user().get("id"))
        self.user_id2 = str(register_user().get("id"))
        self.user_id3 = str(register_user().get("id"))
        self.union_id = generate_union_id()

    def test_bind_multi_account_over_max(self):
        """[用户管理]--绑定第三方账号, 绑定多个账号, 超过上限"""
        path = "/user/bind-third"
        body1 = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": self.user_id1
        }

        resp1 = sdk_http_client.post(path, body1)
        self.assertEqual(resp1.json().get("error_no"), 0)

        body2 = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": self.user_id2
        }
        resp2 = sdk_http_client.post(path, body2)
        self.assertEqual(resp2.json().get("error_no"), 0)

        body3 = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": self.user_id3
        }
        resp3 = sdk_http_client.post(path, body3)
        self.assertNotEqual(resp3.json().get("error_no"), 0)


class TestUnBind(TestCase):

    def setUp(self):
        self.user_id = register_user().get("id")
        self.union_id = generate_union_id()

        bind_third(str(self.user_id), self.union_id)

    def test_unbind_twitter(self):
        """[用户管理]--解绑第三方账号"""
        path = "/user/unbind-third"
        body = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": str(self.user_id)
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_unbind_twitter(self):
        """[用户管理]--解绑第三方账号"""
        path = "/user/unbind-third"
        body = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": str(self.user_id)
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_unbind_twitter_with_empty_body(self):
        """[用户管理]--解绑第三方账号：空表单"""
        path = "/user/unbind-third"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_unbind_twitter_with_blank_body(self):
        """[用户管理]--解绑第三方账号：参数为空"""
        path = "/user/unbind-third"
        body = {
            "type": "",
            "union_id": "",
            "user_id": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_unbind_twitter_with_null_body(self):
        """[用户管理]--解绑第三方账号：参数为null"""
        path = "/user/unbind-third"
        body = {
            "type": None,
            "union_id": None,
            "user_id": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_unbind_twitter_with_part_body_unionid(self):
        """[用户管理]--解绑第三方账号,参数缺失：只传unoinid"""
        path = "/user/unbind-third"
        body = {
            "union_id": self.union_id
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_unbind_twitter_with_part_body_userid(self):
        """[用户管理]--解绑第三方账号,参数缺失：只传userid"""
        path = "/user/unbind-third"
        body = {
            "user_id": str(self.user_id)
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_unbind_twitter_without_type(self):
        """[用户管理]--解绑第三方账号,参数缺失不传类型"""
        path = "/user/unbind-third"
        body = {
            "user_id": str(self.user_id),
            "union_id": self.union_id
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_unbind_twitter_with_invalid_user_id(self):
        """[用户管理]--解绑第三方账号,用户未绑定解绑"""
        path = "/user/unbind-third"
        body = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": "123"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)

    def test_unbind_twitter_with_invalid_union_id(self):
        """[用户管理]--解绑第三方账号,uniondid未绑定解绑"""
        path = "/user/unbind-third"
        body = {
            "type": "2",
            "union_id": "aaa",
            "user_id": str(self.user_id)
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)

    def test_unbind_twitter_with_invalid_type(self):
        """[用户管理]--解绑第三方账号,不存在的type"""
        path = "/user/unbind-third"
        body = {
            "type": "2000",
            "union_id": self.union_id,
            "user_id": str(self.user_id)
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1005)


class TestDuplicateUnBind(TestCase):
    def setUp(self):
        self.user_id = register_user().get("id")
        self.union_id = generate_union_id()
        bind_third(str(self.user_id), self.union_id)

    def test_duplicate_unbind_twitter(self):
        """[用户管理]--绑定第三方账号, 重复解绑报错"""
        path = "/user/unbind-third"
        body = {
            "type": "2",
            "union_id": self.union_id,
            "user_id": str(self.user_id)
        }
        resp1 = sdk_http_client.post(path, body)
        self.assertEqual(resp1.json().get("error_no"), 0)
        resp2 = sdk_http_client.post(path, body)
        # {'error_no': 1005, 'message': '参数无效'}
        self.assertNotEqual(resp2.json().get("error_no"), 0)


class TestBindList(TestCase):
    def setUp(self):
        self.user_id = str(register_user().get("id"))
        self.union_id = generate_union_id()

        bind_third(self.user_id, self.union_id)

    def test_get_bind_list(self):
        """[用户管理]--获取用户已经绑定的第三方账号信息"""
        path = "/user/bind-list"
        body = {
            "user_id": self.user_id
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("is_tw_bind"), "1")

    def test_get_bind_list_with_empty_body(self):
        """[用户管理]--获取用户已经绑定的第三方账号信息,空表单"""
        path = "/user/bind-list"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_get_bind_list_with_blank_body(self):
        """[用户管理]--获取用户已经绑定的第三方账号信息,参数为空"""
        path = "/user/bind-list"
        body = {
            "user_id": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_get_bind_list_with_null_body(self):
        """[用户管理]--获取用户已经绑定的第三方账号信息,参数为null"""
        path = "/user/bind-list"
        body = {
            "user_id": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_get_bind_list_with_invalid_user_id(self):
        """[用户管理]--获取用户已经绑定的第三方账号信息,用户未绑定"""
        path = "/user/bind-list"
        body = {
            "user_id": "123"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertNotEqual(response.json().get("result").get("is_tw_bind"), "1")

