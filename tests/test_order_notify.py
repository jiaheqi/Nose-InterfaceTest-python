from unittest import TestCase

from tests.components.fake import generate_device_id, get_app_id, get_game_id
from tests.components.httpclient import server_http_client, api_server_http_client
from tests.components.tools import time_format_YmdHMS
from tests.components.utils import register_user, google_exchange


class TestOrderNotify(TestCase):
    """
    补发/补单调用同一个接口：1.订单未支付，调用是补发；2.订单已支付，通知失败 调用是补单
    """

    def setUp(self) -> None:
        device = generate_device_id()
        user = register_user(device)
        current_time = time_format_YmdHMS()
        appid = get_app_id()
        game_id = int(get_game_id())
        self.appid = appid
        self.game_id = game_id
        self.current_time = current_time
        self.device = device
        self.account = user.get("account")
        self.user_id = str(user.get("id"))
        self.role_id = f"{self.user_id}_1111"
        self.role_name = f"role_name_{self.user_id}"
        order_id = google_exchange(self.appid, self.device, self.current_time, self.role_id, self.role_name,
                                   self.user_id)
        self.order_id = order_id

    def test_order_notify_with_success_order(self):
        """[admin补发/补单]未支付订单补发/补单+已补发订单重复补发/补单"""
        path = "/api/v1/orders/notify"
        body = {
            "game_id": self.game_id,
            "order_id": self.order_id
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 0)
        response1 = api_server_http_client.post(path, body)
        # {'code': 1, 'message': '订单未支付或者已经通知Game Server，请登录管理后台查看订单支付状态'}
        self.assertEqual(response1.json().get('code'), 1)

    def test_order_notify_with_success_but_not_notify_order(self):
        """[admin补单/补发]已支付但通知失败订单补单"""
        path = f"/api/v1/orders?game_id={self.game_id}&pay_way=2&notify_status=0&pageNumber=1&pageSize=1"
        response = api_server_http_client.get(path)
        order_id = response.json().get('result').get('data')[0].get('order_id')
        path1 = "/api/v1/orders/notify"
        body = {
            "game_id": self.game_id,
            "order_id": order_id
        }
        response1 = api_server_http_client.post(path1, body)
        path2 = f"/api/v1/orders?game_id={self.game_id}&order_id={order_id}"
        response2 = api_server_http_client.get(path2)
        self.assertEqual(response1.json().get('code'), 0)
        # {'code': 1, 'message': '订单未支付或者已经通知Game Server，请登录管理后台查看订单支付状态'}
        self.assertEqual(response2.json().get('result').get('data')[0].get('notify_status'), 1)

    def test_order_notify_with_empty_order(self):
        """[admin补单/补发]不传order_id"""
        path = "/api/v1/orders/notify"
        body = {
            "game_id": self.game_id
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_order_notify_with_blank_order(self):
        """[admin补单/补发]order_id为空"""
        path = "/api/v1/orders/notify"
        body = {
            "game_id": self.game_id,
            "order_id": ""
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_order_notify_with_null_order(self):
        """[admin补单/补发]order_id为null"""
        path = "/api/v1/orders/notify"
        body = {
            "game_id": self.game_id,
            "order_id": None
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_order_notify_with_empty_game_id(self):
        """[admin补单/补发]不传game_id"""
        path = "/api/v1/orders/notify"
        body = {
            "order_id": self.order_id
        }
        response = api_server_http_client.post(path, body)
        # 返回成功，game_id非必须
        self.assertEqual(response.json().get('code'), 0)

    def test_order_notify_with_null_game_id(self):
        """[admin补单/补发]game_id为null"""
        path = "/api/v1/orders/notify"
        body = {
            "game_id": None,
            "order_id": self.order_id
        }
        response = api_server_http_client.post(path, body)
        # 返回成功，game_id非必须
        self.assertEqual(response.json().get('code'), 0)


class TestOrderGet(TestCase):
    def setUp(self) -> None:
        device = generate_device_id()
        user = register_user(device)
        current_time = time_format_YmdHMS()
        appid = get_app_id()
        self.appid = appid
        self.current_time = current_time
        self.device = device
        self.account = user.get("account")
        self.not_exist_account = "0000"
        self.user_id = str(user.get("id"))
        self.role_id = f"{self.user_id}_1111"
        self.not_exist_role_id = "0000"
        self.role_name = f"role_name_{self.user_id}"
        order_id = google_exchange(self.appid, self.device, self.current_time, self.role_id, self.role_name,
                                   self.user_id)
        self.order_id = order_id
        self.not_exist_order_id = "123"
        self.pay_id = "GPA.3330-5464-9384-40093"
        self.not_exist_pay_id = "123"
        game_id = get_game_id()
        self.game_id = game_id
        self.product_id = "com.topjoy.sdk_demo.pay100"
        self.not_exist_product_id = "0000"
        self.server_id = "1"
        self.not_exist_server_id = "0000"
        # 谷歌支付
        self.pay_way = "2"
        self.not_exist_pay_way = "10000"
        # 支付成功
        self.pay_status = "1"
        self.not_exist_pay_status = "10000"
        # 通知成功
        self.notify_status = "1"
        self.not_exist_notify_status = "10000"
        # 测试账号
        self.order_attribute = "1"
        self.not_exist_order_attribute = "0000"

    def test_orders_get_with_order_id(self):
        """[查询订单]根据order_id查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&order_id=" + self.order_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data')[0].get('order_id'), self.order_id)

    def test_orders_get_with_invalid_order_id(self):
        """[查询订单]根据order_id查询订单,查询不存在的订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&order_id=" + self.not_exist_order_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_pay_id(self):
        """[查询订单]根据pay_id查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&pay_id=" + self.pay_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('pay_id'), self.pay_id)

    def test_orders_get_with_invalid_pay_id(self):
        """[查询订单]根据pay_id查询订单,不存在的pay_id"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&pay_id=" + self.not_exist_pay_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_account(self):
        """[查询订单]根据account查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&account=" + self.account
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('account'), self.account)

    def test_orders_get_with_invalid_account(self):
        """[查询订单]根据account查询订单,不存在的account"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&account=" + self.not_exist_account
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_role_id(self):
        """[查询订单]根据role_id查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&role_id=" + self.role_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('role_id'), self.role_id)

    def test_orders_get_with_invalid_role_id(self):
        """[查询订单]根据role_id查询订单,不存在的role_id"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&role_id=" + self.not_exist_role_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_product_id(self):
        """[查询订单]根据product_id查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&product_id=" + self.product_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('product_id'), self.product_id)

    def test_orders_get_with_invalid_product_id(self):
        """[查询订单]根据product_id查询订单,不存在的product_id"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&product_id=" + self.not_exist_product_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_server_id(self):
        """[查询订单]根据server_id查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&server_id=" + self.server_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('server_id'), self.server_id)

    def test_orders_get_with_invalid_server_id(self):
        """[查询订单]根据server_id查询订单,不存在的server_id"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&server_id=" + self.not_exist_server_id
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_pay_way(self):
        """[查询订单]根据pay_way查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&pay_way=" + self.pay_way
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('pay_way'), int(self.pay_way))

    def test_orders_get_with_invalid_pay_way(self):
        """[查询订单]根据pay_way查询订单,不存在的pay_way"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&pay_way=" + self.not_exist_pay_way
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_pay_status(self):
        """[查询订单]根据pay_status查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&pay_status=" + self.pay_status
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('pay_status'), int(self.pay_status))

    def test_orders_get_with_invalid_pay_status(self):
        """[查询订单]根据pay_status查询订单,不存在的pay_status"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&pay_status=" + self.not_exist_pay_status
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_notify_status(self):
        """[查询订单]根据notify_status查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&notify_status=" + self.notify_status
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('notify_status'), int(self.notify_status))

    def test_orders_get_with_invalid_notify_status(self):
        """[查询订单]根据notify_status查询订单,不存在的notify_status"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&notify_status=" + self.not_exist_notify_status
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])

    def test_orders_get_with_order_attribute(self):
        """[查询订单]根据order_attribute查询订单"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&order_attribute=" + self.order_attribute
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result').get('data')[0])
        self.assertEqual(response.json().get('result').get('data')[0].get('order_attribute'), int(self.order_attribute))

    def test_orders_get_with_invalid_order_attribute(self):
        """[查询订单]根据order_attribute查询订单,不存在的order_attribute"""
        path = "/api/v1/orders?game_id=" + self.game_id + "&order_attribute=10000"
        response = api_server_http_client.get(path)
        self.assertEqual(response.json().get('code'), 0)
        self.assertEqual(response.json().get('result').get('data'), [])


class TestOrderGoogleFix(TestCase):
    """
    谷歌支付票据补单
    """

    def setUp(self) -> None:
        self.purchase_token = "eakpihfilaobljpcanbgnaaj.AO-J1Ox1D1ony1pbbcf_i9Dd1lji9IL_q1lMgf3McOr1kRSB2DBs8QwCAKDyXCVEQ5sOhbY1TLSVQcjZDnEXjcgGzoURiXdSwA"
        self.product_id = "com.topjoy.sdk_demo.pay100"
        self.game_id = int(get_game_id())

    def test_google_query(self):
        path = "/api/v1/orders/google_query"
        body = {
            "game_id": self.game_id,
            "product_id": self.product_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result'))

    def test_google_fix(self):
        """[admin谷歌票据补单]已通知成功订单，重复补单"""
        path = "/api/v1/orders/google_fix"
        body = {
            "game_id": self.game_id,
            "product_id": self.product_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_google_fix_with_empty_body(self):
        """[admin谷歌票据补单]空表单"""
        path = "/api/v1/orders/google_fix"
        body = {
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_google_fix_with_blank_body(self):
        """[admin谷歌票据补单]参数为空"""
        path = "/api/v1/orders/google_fix"
        body = {
            "game_id": self.game_id,
            "product_id": "",
            "purchase_token": ""
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_google_fix_with_null_body(self):
        """[admin谷歌票据补单]参数为null"""
        path = "/api/v1/orders/google_fix"
        body = {
            "game_id": None,
            "product_id": None,
            "purchase_token": None
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_google_fix_without_product_id(self):
        """[admin谷歌票据补单]参数缺失，缺少product_id"""
        path = "/api/v1/orders/google_fix"
        body = {
            "game_id": self.game_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_google_fix_without_purchase_token(self):
        """[admin谷歌票据补单]参数缺失，缺少purchase_token"""
        path = "/api/v1/orders/google_fix"
        body = {
            "game_id": self.game_id,
            "product_id": self.product_id
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_google_fix_without_game_id(self):
        """[admin谷歌票据补单]参数缺失，缺少game_id"""
        path = "/api/v1/orders/google_fix"
        body = {
            "product_id": self.product_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)


class TestOrderHuaweiFix(TestCase):
    """
    华为支付票据补单
    """

    def setUp(self) -> None:
        self.purchase_token = "0000018b187700ef48ded97a09af80c4fbcdebb9c8bd4559608772f2088623bfaec0a40511bd14dcx434e.1.109083613"
        self.product_id = "zeusdemo.huawei.product01"
        self.game_id = int(get_game_id())

    def test_huawei_query(self):
        path = "/api/v1/orders/huawei_query"
        body = {
            "game_id": self.game_id,
            "product_id": self.product_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 0)
        self.assertIsNotNone(response.json().get('result'))

    def test_huawei_fix(self):
        """[admin华为票据补单]已成功订单重复补单"""
        path = "api/v1/orders/huawei_fix"
        body = {
            "game_id": self.game_id,
            "product_id": self.product_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_huawei_fix_with_empty_body(self):
        """[admin华为票据补单]空表单"""
        path = "/api/v1/orders/huawei_fix"
        body = {
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_huawei_fix_with_blank_body(self):
        """[admin华为票据补单]参数为空"""
        path = "/api/v1/orders/huawei_fix"
        body = {
            "game_id": self.game_id,
            "product_id": "",
            "purchase_token": ""
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_huawei_fix_with_null_body(self):
        """[admin华为票据补单]参数为null"""
        path = "/api/v1/orders/huawei_fix"
        body = {
            "game_id": None,
            "product_id": None,
            "purchase_token": None
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_huawei_fix_without_product_id(self):
        """[admin华为票据补单]参数缺失，缺少product_id"""
        path = "/api/v1/orders/huawei_fix"
        body = {
            "game_id": self.game_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_huawei_fix_without_purchase_token(self):
        """[admin华为票据补单]参数缺失，缺少purchase_token"""
        path = "/api/v1/orders/huawei_fix"
        body = {
            "game_id": self.game_id,
            "product_id": self.product_id
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)

    def test_huawei_fix_without_game_id(self):
        """[admin华为票据补单]参数缺失，缺少game_id"""
        path = "/api/v1/orders/huawei_fix"
        body = {
            "product_id": self.product_id,
            "purchase_token": self.purchase_token
        }
        response = api_server_http_client.post(path, body)
        self.assertEqual(response.json().get('code'), 1)
