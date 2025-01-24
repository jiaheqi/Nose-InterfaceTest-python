from unittest import TestCase

from tests.components.httpclient import translate_http_client


class TestTranslate(TestCase):
    def test_translate(self):
        """[扩展服务]--翻译文本，正常请求"""
        response = translate_http_client.translate("100", "你好", "en")
        self.assertEqual(response.json(), "Hello")

    def test_translate_with_invalid_target(self):
        """[扩展服务]--翻译文本，异常的目标语言"""
        response = translate_http_client.translate("100", "你好", "xx")
        self.assertEqual(response.json().get("status"), 400)
