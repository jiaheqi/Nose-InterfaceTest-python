import base64
import copy
import hashlib
import json
import time
import unittest
from urllib.parse import urljoin
import requests
from tests.components.fake import *
from tests.components.tools import generate_jwt_token
from retrying import retry


class HTTPClient(object):

    def __init__(self, host):
        self.host = host

    @property
    def headers(self):
        return {
            "content-type": "application/json"
        }

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def post(self, url, body):
        data = copy.copy(body)
        resp = requests.post(urljoin(self.host, url), data=json.dumps(data), headers=self.headers)
        if resp.status_code == 504 or resp.status_code == 502:
            raise Exception(resp.text)
        else:
            return resp


class SDKHTTPClient(object):

    def __init__(self, host, app_id, secret_key):
        self.host = host
        self.app_id = app_id
        self.secret_key = secret_key

    @property
    def headers(self):
        return {
            "content-type": "application/json",
            "client-ip": "106.61.233.174"
        }

    def _sign(self, body):
        sort_keys = sorted(body.keys())
        body_string = ""
        for key in sort_keys:
            body_string += f"{key}{body[key]}"

        body_string += self.secret_key
        return hashlib.md5(body_string.encode("utf-8")).hexdigest()

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def post(self, url, body):
        data = copy.copy(body)
        if "appid" not in data and self.app_id:
            data.update({"appid": self.app_id})
        data.update({"sign": self._sign(data)})
        body_base64 = base64.b64encode(json.dumps(data).encode("ascii"))
        resp = requests.post(urljoin(self.host, url), data=body_base64, headers=self.headers)
        if resp.status_code == 504 or resp.status_code == 502:
            raise Exception(resp.text)
        else:
            return resp


class ServerHTTPClient(object):

    def __init__(self, host, app_id):
        self.host = host
        self.app_id = app_id

    @property
    def headers(self):
        return {
            "content-type": "application/json"
        }

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def post(self, url, body):
        data = copy.copy(body)
        data.update({"appid": self.app_id})
        resp = requests.post(urljoin(self.host, url), data=json.dumps(data), headers=self.headers)
        if resp.status_code == 504 or resp.status_code == 502:
            raise Exception(resp.text)
        else:
            return resp


class ApiServerHTTPClient(object):
    def __init__(self, host, app_id):
        self.host = host
        self.app_id = app_id

    @property
    def headers(self):
        jwt_token = generate_jwt_token()
        return {
            "content-type": "application/json",
            "authorization": jwt_token
        }

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def post(self, url, body):
        data = copy.copy(body)
        data.update({"appid": self.app_id})
        resp = requests.post(urljoin(self.host, url), data=json.dumps(data), headers=self.headers)
        if resp.status_code == 504 or resp.status_code == 502:
            raise Exception(resp.text)
        else:
            return resp

    def get(self, url):
        resp = requests.get(urljoin(self.host, url), headers=self.headers)
        return resp

    def put(self, url, body):
        data = copy.copy(body)
        data.update({"appid": self.app_id})
        resp = requests.put(urljoin(self.host, url), data=json.dumps(data), headers=self.headers)
        return resp

    def delete(self, url, body):
        data = copy.copy(body)
        data.update({"appid": self.app_id})
        resp = requests.delete(urljoin(self.host, url), data=json.dumps(data), headers=self.headers)
        return resp


class TranslateHttpClient(object):

    def __init__(self, host, app_key, app_secret):
        self.host = host
        self.app_key = app_key
        self.app_secret = app_secret

    def generate_md5(self, body, timestamp):
        """
        app_id: 是提供的 secret_key, 一般为项目代号
        token: 是提供的 secret_value 密钥
        body: 表单内容 {"app_id": "test", "user_id": "11", "target": "en", "content": "你好啊
    "}
        *** token在前content在后 ***
        """
        md = hashlib.md5()
        text = f"{self.app_secret}:{body['app_id']}-{body['user_id']}-{body['target']}-{body['content']}-{timestamp}"
        md.update(f"{text}".encode())
        return f"{body['app_id']}:{md.hexdigest()}"

    def translate(self, user_id, text, target):
        body = {
            "app_id": self.app_key,
            "user_id": user_id,
            "target": target,
            "content": text
        }
        timestamp = str(int(time.time()))
        headers = {"Content-Type": "application/json",
                   "Signature": self.generate_md5(body, timestamp),
                   "timestamp": timestamp
                   }

        return requests.post(self.host, data=json.dumps(body), headers=headers)


class TkwServerHTTPClient:
    def __init__(self, host):
        self.host = host

    @property
    def headers(self):
        return {
            "content-type": "application/json"
        }

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def post(self, url, body):
        data = copy.copy(body)
        resp = requests.post(urljoin(self.host, url), data=json.dumps(data), headers=self.headers)
        return resp
        if resp.status_code == 504 or resp.status_code == 502:
            raise Exception(resp.text)
        else:
            return resp


http_client = HTTPClient(
    get_host(),
)
sdk_http_client = SDKHTTPClient(
    get_host(),
    get_app_id(),
    get_secret_key()
)
another_sdk_http_client = SDKHTTPClient(
    get_host(),
    get_app_id_another(),
    get_secret_key_another()
)
server_http_client = ServerHTTPClient(
    get_host(),
    get_app_id()
)

api_server_http_client = ApiServerHTTPClient(
    get_host(),
    get_app_id()
)

translate_http_client = TranslateHttpClient(
    "https://parrot.topjoy.com/rpc/translate",
    "test",
    "ee93339c48b36552e94b6e1ff6f9119d"
)

tkw_http_client = TkwServerHTTPClient(
    "https://tkw-pay.youle.game"
)
