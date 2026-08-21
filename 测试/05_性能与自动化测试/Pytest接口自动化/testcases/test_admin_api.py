# -*- coding: utf-8 -*-
"""管理后台接口自动化用例（权限/用户状态/商品状态）。"""
import pytest

from utils import assertions
from utils.data_factory import new_user

pytestmark = pytest.mark.regression


def test_admin_list_users_success(admin_client):
    """正常：管理员获取用户列表。"""
    r = admin_client.get("/api/admin/users", params={"page": 1, "size": 10})
    assertions.assert_success(r)


def test_normal_user_forbidden_admin(client):
    """安全：普通用户访问管理接口 → 403。"""
    client.register_and_login(new_user())
    r = client.get("/api/admin/users")
    assertions.assert_biz_error(r, 403, "无管理员权限")


def test_admin_disable_user_blocks_login(client, admin_client):
    """数据：管理员禁用用户后，该用户无法登录。"""
    # 注册一个新用户
    user = new_user()
    assertions.assert_success(client.post("/api/users/register", json=user))
    me = client.login(user["username"], user["password"])
    uid = me.body["id"]

    # 管理员禁用
    assertions.assert_success(admin_client.put("/api/admin/users/%s/status" % uid, json={"status": 0}))

    # 禁用后无法登录
    r = client.login(user["username"], user["password"])
    assertions.assert_biz_error(r, 400, "账号已被禁用")


def test_admin_update_item_status(client, admin_client):
    """功能：管理员修改商品状态（下架）。"""
    # 普通用户发布商品
    c = client
    c.register_and_login(new_user())
    item_id = c.post("/api/items", json={"title": "待管理审核商品", "categoryId": 1, "price": 10}).body["id"]

    # 管理员审核通过
    assertions.assert_success(admin_client.put("/api/admin/items/%s/status" % item_id, json={"status": 1}))
    r = c.get("/api/items/%s" % item_id)
    assertions.assert_success(r)
    assert r.body["status"] == 1, "审核通过后商品状态应为在售"
