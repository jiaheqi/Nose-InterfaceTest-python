import hashlib
import time
from datetime import datetime, timedelta

import jwt
import requests

"""
工具类
"""


def time_format_YmdHMS():
    current_time = datetime.now()
    format_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return format_time


def time_format_timestamp_second():
    """
    :return: 当前时间时间戳：秒为单位
    """
    current_timestamp = int(time.time())
    return current_timestamp


def time_format_timestamp_ms():
    """
    :return: 当前时间时间戳：毫秒为单位
    """
    current_timestamp = int(time.time() * 1000)
    return current_timestamp


def time_format_timestamp_expire_date_ms():
    """
    :return:未来一段时间的时间戳（用于到期时间）：毫秒为单位
    """
    current_time = datetime.now()
    time_interval = timedelta(days=365)
    future_time = current_time+time_interval
    future_timestamp = int(future_time.timestamp())
    return future_timestamp


def generate_jwt_token():
    """
    :return: 生成admin后台接口请求所需要的headers中的token
    """
    JWT_SECRET_KEY = "topjoy"
    JWT_ALGORITHM = "HS256"
    future_timestamp = time_format_timestamp_expire_date_ms()
    user_data = {
        "User": {
            "name": 'chaos',
            "user_id": '999999',
            "is_admin": True,
            "allow_games": [{"alias": "opsgametest", "en_name": "admin"}],
        },
        "exp": future_timestamp,
        "iss": "zeus"
    }
    jwt_token = jwt.encode(user_data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jwt_token


def retry(max_retries=3, delay_seconds=5):
    """
    装饰器函数，用于在失败时重试函数调用。
    Args:
        max_retries (int): 最大重试次数。
        delay_seconds (int): 重试之间的延迟秒数。
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    response = func(*args, **kwargs)
                    if response.status_code == 504 or response.status_code == 502:
                        print(f"重试 {retries + 1}/{max_retries}: 返回状态码 504or502")
                        time.sleep(delay_seconds)
                        retries += 1
                    else:
                        return response  # 如果不是 504，立即返回响应
                except requests.exceptions.RequestException as e:
                    print(f"重试 {retries + 1}/{max_retries}: {e}")
                    time.sleep(delay_seconds)
                    retries += 1
            raise Exception(f"最大重试次数 ({max_retries}) exceeded")
        return wrapper
    return decorator
