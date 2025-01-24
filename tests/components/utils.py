import json

from tests.components.httpclient import sdk_http_client, api_server_http_client
from tests.components.fake import *


def register_user(device=generate_device_id()):
    path = "/user/register"
    body = {
        "device": device,
        "mobile_info": json.dumps(generate_mobile_info()),
        "platform": "ios",
    }

    response = sdk_http_client.post(path, body)
    return response.json().get("result")


def user_login(account, device):
    path = "/user/login"
    body = {
        "account": account,
        "device": device
    }
    response = sdk_http_client.post(path, body)
    return response.json().get("result")


def bind_third(user_id, union_id):
    bind_path = "/user/bind-third"
    bind_body = {
        "type": "2",
        "union_id": union_id,
        "user_id": user_id
    }

    sdk_http_client.post(bind_path, bind_body)


def create_ios_order(user_id):
    path = "/order/ios-exchange"
    body = {
        "user_id": user_id,
        "role_id": "123",
        "product_id": "123",
        "price": "123",
        "extend": "123",
        "device": "123",
        "role_name": "123"
    }

    response = sdk_http_client.post(path, body)
    return response.json().get("result")


def role_save(device, user_id, role_id, role_name):
    path = "/role/save"
    body = {
        "device": device,
        "platform": "ios",
        "level": "12",
        "server_name": "server_name",
        "server_id": "1111",
        "role_id": role_id,
        "user_id": str(user_id),
        "role_name": role_name,
        "vip": "5"
    }
    response = sdk_http_client.post(path, body)
    return response.json().get("result")


def get_game_account_modules(accountModule_label, accountConfigs_label):
    """
    :param accountConfigs_label:
    :param accountModule_label: 当前登录方式：AppleID
    :return: 返回当前登录方式的开关状态，当前登录方式的参数值
    """
    game_id = get_game_id()
    path = "/api/v1/game/accounts?game_id="+game_id
    account_modules = api_server_http_client.get(path).json().get('result').get(
        'account_modules')
    account_module = [account_module for account_module in account_modules if
                      account_module.get('accountModule').get('label') == accountModule_label]
    open_status = account_module[0].get('accountModule').get('is_login_open')
    accountConfigs = account_module[0].get('accountConfigs')
    json_obj = [json_obj for json_obj in accountConfigs if json_obj.get('label') == accountConfigs_label]
    value = json_obj[0].get('value')
    return open_status, value


def google_exchange(appid, device, extend, role_id, role_name, user_id):
    path = "/order/google-exchange"
    body = {
        "appid": appid,
        "device": device,
        "extend": extend,
        "lang": "1",
        "level": "5",
        "pay_notify_url": get_notify_url(),
        "platform": "android",
        "price": "99",
        "product_id": "com.topjoy.sdk_demo.pay100",
        "role_id": role_id,
        "role_name": role_name,
        "sdk_version": "2.8.4-SNAPSHOT",
        "server_id": "1",
        "server_name": "serverName",
        "user_id": user_id,
        "vip": "1"
    }
    response = sdk_http_client.post(path, body)
    return response.json().get('result').get('order_id')





