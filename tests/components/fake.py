import os

import uuid


def get_app_id():
    return os.getenv('APP_ID')


def get_secret_key():
    return os.getenv('SECRET_KEY')


def get_app_id_another():
    return os.getenv('APP_ID_ANOTHER')


def get_secret_key_another():
    return os.getenv('SECRET_KEY_ANOTHER')


def get_host():
    return os.getenv('HOST')


def get_game_id():
    return os.getenv('GAME_ID')


def get_notify_url():
    return os.getenv('NOTIFY_URL')


def get_ios_transaction_id():
    return os.getenv('IOS_TRANSACTION_ID')


def generate_third_login_token():
    return str(uuid.uuid4()).upper()


def generate_device_id():
    return str(uuid.uuid4()).upper()


def generate_union_id():
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
