import json
from unittest import TestCase

from tests.components.fake import get_app_id
from tests.components.httpclient import sdk_http_client

"""
[游戏信息]--初始化，获取游戏信息
参数校验：
1.空表单
2.参数为空或者null
3.参数缺失，只传部分参数
4.appid不存在
正常/异常：
1.正常验证+返回值校验
"""


class TestGameInfo(TestCase):
    def test_get_game_info_with_empty_body(self):
        """[游戏信息]--获取游戏信息，空表单"""
        path = "/game/info"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)

    def test_get_game_info_with_blank_body(self):
        """[游戏信息]--获取游戏信息，参数为空"""
        path = "/game/info"
        body = {
            "appid": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_get_game_info_with_null_body(self):
        """[游戏信息]--获取游戏信息，参数为null"""
        path = "/game/info"
        body = {
            "appid": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_get_game_info(self):
        """[游戏信息]--获取游戏信息"""
        path = "/game/info"
        body = {
            "appid": get_app_id()
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertIn("message", response.json())
        self.assertIn("result", response.json())

    def test_get_game_info_with_not_exist_appid(self):
        """[游戏信息]--获取游戏信息, 不存在的appid"""
        path = "/game/info"
        body = {
            "appid": "123456"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)
