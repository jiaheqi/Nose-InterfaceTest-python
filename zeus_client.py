import base64
import hashlib

import uuid
import json

from urllib.parse import urljoin

import requests

TWITTER_UNION_ID = "9644758786116689921"


class ThirdLoginType(object):
    FACEBOOK = "1"
    TWITTER = "2"


def generate_device_id():
    return str(uuid.uuid4()).upper()


def generate_mobile_info():
    return {
        "country_code": "zh",
        "system_name": "iOS",
        "model": "xPhone",
        "device_id": str(uuid.uuid4()).upper(),
        "os_version": "16.0",
        "network": "Wifi"
    }


class ZeusClient(object):

    def __init__(self, host, app_id, secret_key):
        self.host = host
        self.app_id = app_id
        self.secret_key = secret_key

    @property
    def headers(self):
        return {
            "content-type": "application/json"
        }

    def _sign(self, body):
        sort_keys = sorted(body.keys())
        body_string = ""
        for key in sort_keys:
            body_string += f"{key}{body[key]}"

        body_string += self.secret_key
        return hashlib.md5(body_string.encode("utf-8")).hexdigest()

    def post(self, url, body):
        body.update({"appid": self.app_id})
        # body.update({"sign": self._sign(body)})
        # body_base64 = base64.b64encode(json.dumps(body).encode("ascii"))
        print(json.dumps(body))
        resp = requests.post(urljoin(self.host, url), data=json.dumps(body), headers=self.headers)
        return resp

    def v2_third_login(self):
        path = "/v2/user/third-login"
        body = {
            "device": "123",
            "mobile_info": json.dumps(generate_mobile_info()),
            "platform": "ios",
            "secret_token": "YNn9kbVpG3ye0GfekklRvfY3uFNodl53YUWZSEgSZt1Zo",
            "token": "1448258638015975434-KV490zlLWf0E5bvMhSTiv9ASWoWkYO",
            "type": ThirdLoginType.TWITTER,
            "union_id": TWITTER_UNION_ID
        }
        resp = self.post(path, body)
        return resp.json()

    def get_game_info(self):
        path = "/game/info"
        body = {}
        resp = self.post(path, body)
        return resp.json()

    def antispam_test_check(self):
        path = "/antispam/text-check"
        body = {
            "data_id": "123456",
            "data": "你好"
        }
        resp = self.post(path, body)
        return resp.text

    def server_antispam_test_check(self):
        path = "/server/antispam/text-check"
        body = {
            "data_id": "123456",
            "data": "Hello fuck"
        }
        resp = self.post(path, body)
        return resp.text

    def login_verify(self):
        path = "/login/verify"
        body = {
            "user_id": "995359097",
            "token": "JLBHVXwMKMrdvVTypejGlffyqIcTZYuB"
        }
        resp = self.post(path, body)
        return resp.text

if __name__ == "__main__":
    zeus_client = ZeusClient(
        # "http://0.0.0.0:8000",
        # "https://abroad.topjoy.com",
        "https://zeus.youle.game",
        "GEPM053N83EU",
        "HJAC8JACS3M1X7T8"
    )
    print(zeus_client.server_antispam_test_check())
