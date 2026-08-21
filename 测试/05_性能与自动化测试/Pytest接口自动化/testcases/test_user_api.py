# -*- coding: utf-8 -*-
"""用户模块接口自动化用例（注册/登录/登出/会话）。"""
import pytest

import config
from utils import assertions
from utils.data_factory import new_user

pytestmark = pytest.mark.regression


def test_register_success(client):
    """正常注册：全部字段合法 → 注册成功。"""
    r = client.post("/api/users/register", json=new_user())
    assertions.assert_success(r)


def test_register_duplicate_username(client):
    """异常注册：用户名重复 → 400。"""
    user = new_user()
    assertions.assert_success(client.post("/api/users/register", json=user))
    r = client.post("/api/users/register", json=user)
    assertions.assert_biz_error(r, 400, "用户名已被注册")


def test_register_short_password(client):
    """边界注册：密码小于6位 → 400。"""
    r = client.post("/api/users/register", json=new_user(password="12345"))
    assertions.assert_biz_error(r, 400, "密码")


def test_register_missing_nickname(client):
    """异常注册：昵称为空 → 400。"""
    r = client.post("/api/users/register", json=new_user(nickname=""))
    assertions.assert_biz_error(r, 400, "昵称不能为空")


def test_login_success(client):
    """正常登录：正确账密 → 成功且不返回密码。"""
    user = new_user()
    assertions.assert_success(client.post("/api/users/register", json=user))
    r = client.login(user["username"], user["password"])
    assertions.assert_success(r)
    assertions.assert_no_password(r)


def test_login_wrong_password(client):
    """异常登录：密码错误 → 400。"""
    user = new_user()
    client.post("/api/users/register", json=user)
    r = client.login(user["username"], "wrong123")
    assertions.assert_biz_error(r, 400, "用户名或密码错误")


def test_login_nonexistent_user(client):
    """异常登录：用户不存在 → 400。"""
    r = client.login("no_such_user_%s" % config.USER_PASSWORD, "123456")
    assertions.assert_biz_error(r, 400, "用户名或密码错误")


def test_logout_then_access_me(client, logged_user):
    """会话：登出后访问个人信息 → 401。"""
    c = logged_user["client"]
    assertions.assert_success(c.post("/api/users/logout"))
    r = c.get("/api/users/me")
    assertions.assert_biz_error(r, 401, "请先登录")
