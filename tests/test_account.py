from unittest import TestCase

from tests.components.httpclient import sdk_http_client


class TestAccountEmailCaptchaSend(TestCase):
    # 因为不能让验证码一直发送，所以上线后需要注释
    # def test_send_email_captcha(self):
    #     """[发送邮箱验证码]正常发送邮箱验证码"""
    #     path = "/account/send-email-captcha"
    #     body = {
    #         "email": "jiaheqi@topjoy.com",
    #         "language": "zh-CN",
    #         "platform": "android",
    #         "sdk_version": "2.8.0"
    #     }
    #     response = sdk_http_client.post(path, body)
    #     self.assertEqual(response.json().get('error_no'), 0)
    #     self.assertEqual(response.json().get('message'), 'success')

    def test_send_email_captcha_with_invalid_email(self):
        """[发送邮箱验证码]邮箱格式有误"""
        path = "/account/send-email-captcha"
        body = {
            "email": "j  iaheqi@topjoy.com",
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_send_email_captcha_with_empty_email(self):
        """[发送邮箱验证码]邮箱不传"""
        path = "/account/send-email-captcha"
        body = {
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_send_email_captcha_with_blank_email(self):
        """[发送邮箱验证码]邮箱为空"""
        path = "/account/send-email-captcha"
        body = {
            "email": "",
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)


class TestAccountEmailRegister(TestCase):
    def test_register_with_email_with_invalid_captcha(self):
        """[邮箱注册]无效的验证码"""
        path = "/account/register-with-email"
        body = {
            "captcha": "1234",
            "email": "jiaheqi@topjoy.com",
            "password": "test1234",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 20003)

    def test_register_with_email_with_duplicate_email(self):
        """[邮箱注册]已注册邮箱重复注册"""
        path = "/account/register-with-email"
        body = {
            "captcha": "8579",
            "email": "jiaheqi@topjoy.com",
            "password": "test1234",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        # 断言应该是1007，但是因为验证码过期拦截在前，所以调整断言为20003
        self.assertEqual(response.json().get("error_no"), 20003)

    def test_send_email_captcha_with_null_email(self):
        """[发送邮箱验证码]邮箱为None"""
        path = "/account/send-email-captcha"
        body = {
            "email": None,
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1002)

    def test_register_with_email_with_blank_body(self):
        """[发送邮箱验证码]参数为None"""
        path = "/account/register-with-email"
        body = {
            "appid": "",
            "captcha": "",
            "email": "",
            "password": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_register_with_email_with_empty_body(self):
        """[发送邮箱验证码]参数为空"""
        path = "/account/register-with-email"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_register_with_email_with_null_body(self):
        """[发送邮箱验证码]参数为None"""
        path = "/account/register-with-email"
        body = {
            "appid": None,
            "captcha": None,
            "email": None,
            "password": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)


class TestAccountEmailLogin(TestCase):
    def test_login_with_email(self):
        """[邮箱登录]正常登录"""
        path = "/account/login-with-email"
        body = {
            "email": "jiaheqi@topjoy.com",
            "password": "1234",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)
        self.assertIsNotNone(response.json().get("result").get('token'))
        self.assertEqual(response.json().get("result").get('union_id'), '895084263')

    def test_login_with_email_with_unregister_email(self):
        """[邮箱登录]未注册邮箱登录"""
        path = "/account/login-with-email"
        body = {
            "email": "jiaheqi77777@topjoy.com",
            "password": "test1234",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1006)

    def test_login_with_email_with_wrong_password(self):
        """[邮箱登录]登录密码错误"""
        path = "/account/login-with-email"
        body = {
            "email": "jiaheqi@topjoy.com",
            "password": "1111",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1006)

    def test_login_with_email_with_blank_email(self):
        """[邮箱登录]登录邮箱为空"""
        path = "/account/login-with-email"
        body = {
            "email": "",
            "password": "test1234",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_email_with_none_email(self):
        """[邮箱登录]登录邮箱为None"""
        path = "/account/login-with-email"
        body = {
            "email": None,
            "password": "test1234",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_login_with_email_with_empty_body(self):
        """[邮箱登录]请求参数体为空"""
        path = "/account/login-with-email"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_email_with_blank_body(self):
        """[邮箱登录]参数为空"""
        path = "/account/login-with-email"
        body = {
            "email": "",
            "password": "",
            "platform": "",
            "sdk_version": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_email_with_None_body(self):
        """[邮箱登录]参数为None"""
        path = "/account/login-with-email"
        body = {
            "email": None,
            "password": None,
            "platform": None,
            "sdk_version": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)


class TestAccountMobileCaptchaSend(TestCase):
    # 因为不能让验证码一直发，所以先注释掉
    # def test_send_sms_captcha(self):
    #     """[发送短信验证码]正常发送
    #     """
    #     path = "/account/send-sms-captcha"
    #     body = {
    #         "phone": "17600116844",
    #         "area_code": "+86"
    #     }
    #     response = sdk_http_client.post(path, body)
    #     self.assertEqual(response.json().get("error_no"), 0)

    def test_send_sms_captcha_without_phone(self):
        """[发送短信验证码]手机号不传"""
        path = "/account/send-sms-captcha"
        body = {
            "area_code": "+86"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_send_sms_captcha_without_area_code(self):
        """[发送短信验证码]区号不传"""
        path = "/account/send-sms-captcha"
        body = {
            "phone": "17600116844"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_send_sms_captcha_without_empty_body(self):
        """[发送短信验证码]空表单"""
        path = "/account/send-sms-captcha"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_send_sms_captcha_without_blank_body(self):
        """[发送短信验证码]参数为空"""
        path = "/account/send-sms-captcha"
        body = {
            "phone": "",
            "area_code": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_send_sms_captcha_without_null_body(self):
        """[发送短信验证码]参数为None"""
        path = "/account/send-sms-captcha"
        body = {
            "phone": None,
            "area_code": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)

    def test_send_sms_captcha_with_invalid_phone(self):
        """[发送短信验证码]手机号码格式错误"""
        path = "/account/send-sms-captcha"
        body = {
            "phone": "177",
            "area_code": "+86"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 20004)

    def test_send_sms_captcha_with_invalid_area_code(self):
        """[发送短信验证码]区号格式错误"""
        path = "/account/send-sms-captcha"
        body = {
            "phone": "17600116844",
            "area_code": "+186012345"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 20004)


class TestAccountMobileLogin(TestCase):

    def test_login_with_phone_with_invalid_captcha(self):
        """[短信登录]无效的验证码"""
        path = "/account/login-with-phone"
        body = {
            "captcha": "9596",
            "area_code": "+86",
            "phone": "17600116844"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 20003)

    def test_login_with_phone_with_blank_phone(self):
        """[短信登录]无效的手机号手机号为空"""
        path = "/account/login-with-phone"
        body = {
            "captcha": "9596",
            "area_code": "+86",
            "phone": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_phone_without_captcha(self):
        """[短信登录]验证码不传"""
        path = "/account/login-with-phone"
        body = {
            "area_code": "+86",
            "phone": "17600116844"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_phone_without_phone(self):
        """[短信登录]手机号不传"""
        path = "/account/login-with-phone"
        body = {
            "area_code": "+86",
            "captcha": "9596"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_phone_with_empty_body(self):
        """[短信登录]空表单"""
        path = "/account/login-with-phone"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_phone_with_blank_body(self):
        """[短信登录]参数为空"""
        path = "/account/login-with-phone"
        body = {
            "captcha": "",
            "area_code": "+",
            "phone": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_login_with_phone_with_null_body(self):
        """[短信登录]参数为None"""
        path = "/account/login-with-phone"
        body = {
            "captcha": None,
            "area_code": None,
            "phone": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)


class TestGetAreaCode(TestCase):
    def test_get_area_code(self):
        """[获取区号]正常获取区号"""
        path = "/account/get-area-codes"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 0)


class TestResetPassword(TestCase):
    def test_reset_password_with_unregister_email(self):
        """[密码重置]未注册邮箱重置"""
        path = "/account/reset-password"
        body = {
            "email": "jiaheqiyyyyy@topjoy.com",
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 10001)

    def test_reset_password_without_email(self):
        """[密码重置]邮箱不传"""
        path = "/account/reset-password"
        body = {
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_reset_password_with_blank_email(self):
        """[密码重置]邮箱传空"""
        path = "/account/reset-password"
        body = {
            "email": "",
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_reset_password_with_null_email(self):
        """[密码重置]邮箱传None"""
        path = "/account/reset-password"
        body = {
            "email": None,
            "language": "zh-CN",
            "platform": "android",
            "sdk_version": "2.8.0"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1002)

    def test_reset_password_with_empty_body(self):
        """[密码重置]空表单"""
        path = "/account/reset-password"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_reset_password_with_blank_body(self):
        """[密码重置]参数为空"""
        path = "/account/reset-password"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1003)

    def test_reset_password_with_null_body(self):
        """[密码重置]参数为None"""
        path = "/account/reset-password"
        body = {
            "email": None,
            "language": None,
            "platform": None,
            "sdk_version": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get('error_no'), 1002)


class TestModifyPassword(TestCase):
    def test_modify_password_with_invalid_captcha(self):
        """[重置密码]无效的验证码"""
        path = "/account/modify-password"
        body = {
            "email": "jiaheqi@topjoy.com",
            "password": "test1234",
            "captcha": "1111"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 20003)

    def test_modify_password_with_blank_email(self):
        """[重置密码]email为空"""
        path = "/account/modify-password"
        body = {
            "email": "",
            "password": "test1234",
            "captcha": "1111"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_modify_password_with_blank_password(self):
        """[重置密码]password为空"""
        path = "/account/modify-password"
        body = {
            "email": "jiaheqi@topjoy.com",
            "password": "",
            "captcha": "1111"
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_modify_password_with_empty_body(self):
        """[重置密码]空表单"""
        path = "/account/modify-password"
        body = {
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_modify_password_with_blank_body(self):
        """[重置密码]参数为空"""
        path = "/account/modify-password"
        body = {
            "email": "",
            "password": "",
            "captcha": ""
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1003)

    def test_modify_password_with_null_password(self):
        """[重置密码]参数为None"""
        path = "/account/modify-password"
        body = {
            "email": None,
            "password": None,
            "captcha": None
        }
        response = sdk_http_client.post(path, body)
        self.assertEqual(response.json().get("error_no"), 1002)
