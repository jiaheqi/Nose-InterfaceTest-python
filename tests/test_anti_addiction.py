from datetime import datetime
from unittest import TestCase

import json
from tests.components.httpclient import sdk_http_client
from tests.components.fake import generate_mobile_info, generate_device_id, generate_union_id
from tests.components.utils import register_user


def can_play():
    now = datetime.now()
    if now.weekday() in [4, 5, 6] and now.hour == 20:
        return True
    else:
        return False


"""[防沉迷]--用户实名认证
参数校验：
1.表单为空
2.参数为空或者null
3.参数缺失：缺少id_no,name,account
4.id_no不合法,id_no传空
5.name为空
6.id_no和name不匹配
正常/异常：
1.正常请求
"""
"""[防沉迷]--支付限额
参数校验：
1.表单为空
2.参数为空或者null
正常/异常：
1.正常请求
2.未实名，无配额
3.已实名，成人，无限额
4.已实名，未成年，有限额
"""
"""[防沉迷]--游戏许可
参数校验：
1.表单为空
2.参数为空或者null
正常/异常：
1.正常请求
2.未实名，有限制
3.已实名，成人，无限制
"""


class TestIdentityCheck(TestCase):

    def setUp(self) -> None:
        self.device = generate_device_id()
        user = register_user(self.device)
        self.account = user.get("account")

    def test_user_anti_addiction_check(self):
        """[防沉迷]--用户实名认证, 成年人"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "522601196404090816",
            "name": "王华平",
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("Res"), True)

    def test_user_anti_addiction_check_with_empty_body(self):
        """[防沉迷]--用户实名认证, 空表单"""
        path = "/anti-addiction/identity-check"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_anti_addiction_chec_with_blank_body(self):
        """[防沉迷]--用户实名认证, 参数为空"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": "",
            "id_no": "",
            "name": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_anti_addiction_check_with_null_body(self):
        """[防沉迷]--用户实名认证, 参数为null"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": None,
            "id_no": None,
            "name": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_user_anti_addiction_check_miss_id_no(self):
        """[防沉迷]--用户实名认证, 缺少Id_no"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "name": "王华平",
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_anti_addiction_check_empty_id_no(self):
        """[防沉迷]--用户实名认证, 空Id_no"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "name": "王华平",
            "id_no": ""
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_anti_addiction_check_invalid_id_no(self):
        """[防沉迷]--用户实名认证, 不合法的Id_no"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "name": "王华平",
            "id_no": "123"
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 30001)

    def test_user_anti_addiction_check_miss_name(self):
        """[防沉迷]--用户实名认证, name不传"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "522601196404090816",
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_anti_addiction_check_empty_name(self):
        """[防沉迷]--用户实名认证, 空name"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "522601196404090816",
            "name": ""
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_anti_addiction_check_error_info(self):
        """[防沉迷]--用户实名认证, 不匹配的姓名和ID_No"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "name": "张三",
            "id_no": "522601196404090816"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("Res"), False)

class TestIdentityCheckChild(TestCase):
    def setUp(self) -> None:
        self.device = generate_device_id()
        user = register_user(self.device)
        self.account = user.get("account")

    def test_user_anti_addiction_check_child(self):
        """[防沉迷]--用户实名认证, 未成年人认证：8-16岁"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "110105201112267716",
            "name": "芦泽栋",
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("Res"), True)


class TestPayLimit(TestCase):
    def setUp(self) -> None:
        self.device = generate_device_id()
        user = register_user(self.device)
        self.account = user.get("account")

    def test_user_pay_limit_no_remaining(self):
        """[防沉迷]--支付限额, 未实名，无支付配额"""
        path = "/anti-addiction/pay-limit"
        body = {
            "account": self.account,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("transaction_limit"), 0)
        self.assertLessEqual(response.json().get("result").get("remaining_amount"), 0)

    def test_user_pay_limit_with_empty_body(self):
        """[防沉迷]--支付限额, 空表单"""
        path = "/anti-addiction/pay-limit"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_pay_limit_with_blank_body(self):
        """[防沉迷]--支付限额, 参数为空"""
        path = "/anti-addiction/pay-limit"
        body = {
            "account": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_pay_limit_with_null_body(self):
        """[防沉迷]--支付限额, 参数为null"""
        path = "/anti-addiction/pay-limit"
        body = {
            "account": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)


class TestPayLimitUnLimit(TestCase):
    def setUp(self) -> None:
        self.device = generate_device_id()
        user = register_user(self.device)
        self.account = user.get("account")

    def test_user_pay_limit(self):
        """[防沉迷]--支付限额, 成人实名，无限额"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "522601196404090816",
            "name": "王华平",
        }

        sdk_http_client.post(path, body)

        path = "/anti-addiction/pay-limit"
        body = {
            "account": self.account,
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("transaction_limit"), 2147483648)
        self.assertEqual(response.json().get("result").get("remaining_amount"), 2147483648)


class TestPayLimitHasLimit(TestCase):
    def setUp(self) -> None:
        self.device = generate_device_id()
        user = register_user(self.device)
        self.account = user.get("account")

    def test_user_under_age_pay_limit(self):
        """[防沉迷]--支付限额, 未成年实名，限额"""

        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "110105201112267716",
            "name": "芦泽栋",
        }

        sdk_http_client.post(path, body)

        path = "/anti-addiction/pay-limit"
        body = {
            "account": self.account,
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("transaction_limit"), 5000)
        self.assertNotEquals(response.json().get("result").get("remaining_amount"), 2147483648)


class TestPlayAble(TestCase):
    def setUp(self) -> None:
        self.device = generate_device_id()
        user = register_user(self.device)
        self.account = user.get("account")

    def test_user_play_able_without_(self):
        """[防沉迷]--游玩许可, 未实名，检查是否可玩"""
        path = "/anti-addiction/playable"
        body = {
            "account": self.account,
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("can_play"), can_play())

    def test_user_play_able_true(self):
        """[防沉迷]--游玩许可, 已实名，成人，可玩，不受限制"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "522601196404090816",
            "name": "王华平",
        }
        sdk_http_client.post(path, body)
        path = "/anti-addiction/playable"
        body = {
            "account": self.account
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("can_play"), True)

    def test_user_play_able_false(self):
        """[防沉迷]--游玩许可, 已实名，未成年人，不可玩，游玩受限"""
        path = "/anti-addiction/identity-check"
        body = {
            "account": self.account,
            "id_no": "110105201112267716",
            "name": "芦泽栋",
        }
        sdk_http_client.post(path, body)
        path = "/anti-addiction/playable"
        body = {
            "account": self.account
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("can_play"), can_play())

    def test_user_play_able_with_empty_body(self):
        """[防沉迷]--游玩许可, 空表单"""
        path = "/anti-addiction/playable"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_play_able_with_blank_body(self):
        """[防沉迷]--游玩许可,参数为空"""
        path = "/anti-addiction/playable"
        body = {
            "account": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_user_play_able_with_null_body(self):
        """[防沉迷]--游玩许可, 参数为null"""
        path = "/anti-addiction/playable"
        body = {
            "account": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)
