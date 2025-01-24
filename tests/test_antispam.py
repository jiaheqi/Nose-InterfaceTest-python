from unittest import TestCase

from tests.components.httpclient import sdk_http_client
from tests.components.fake import generate_device_id

"""[内容安全]--服务端屏蔽字检查
参数校验：
1.表单为空
2.参数为空或者null
正常/异常：
1.正常请求，不拦截，全文通过
2.全文拒绝
3.部分通过，部分拒绝
"""


class TestAntispam(TestCase):

    def test_antispam_check(self):
        """[内容安全]--服务端屏蔽字检查, 内容通过"""
        path = "/antispam/text-check"
        body = {
            "data_id": generate_device_id(),
            "data": "text",
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("check_ret"), 0)
        self.assertEqual(response.json().get("result").get("punish_type"), 0)
        self.assertEqual(response.json().get("result").get("result"), "text")

    def test_antispam_check_punish_all(self):
        """[内容安全]--服务端屏蔽字检查, 异常，全文拒绝"""
        path = "/antispam/text-check"
        body = {
            "data_id": generate_device_id(),
            "data": "fuck",
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("check_ret"), 2)
        self.assertEqual(response.json().get("result").get("punish_type"), 1)
        self.assertEqual(response.json().get("result").get("result"), "")

    def test_antispam_check_punish_apart(self):
        """[内容安全]--服务端屏蔽字检查, 异常，部分拒绝"""
        path = "/antispam/text-check"
        body = {
            "data_id": generate_device_id(),
            "data": "Hi fuck",
        }

        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertEqual(response.json().get("result").get("check_ret"), 1)
        self.assertEqual(response.json().get("result").get("punish_type"), 1)
        self.assertEqual(response.json().get("result").get("result"), "")

    def test_antispam_check_with_empty_body(self):
        """[内容安全]--服务端屏蔽字检查, 空表单"""
        path = "/antispam/text-check"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_antispam_check_with_blank_body(self):
        """[内容安全]--服务端屏蔽字检查, 参数为空"""
        path = "/antispam/text-check"
        body = {
            "data_id": "",
            "data": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_antispam_check_with_null_body(self):
        """[内容安全]--服务端屏蔽字检查, 参数为null"""
        path = "/antispam/text-check"
        body = {
            "data_id": None,
            "data": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

