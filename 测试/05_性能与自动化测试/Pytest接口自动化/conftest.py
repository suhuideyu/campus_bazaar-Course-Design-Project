# -*- coding: utf-8 -*-
"""pytest 全局 fixtures：客户端、登录用户、卖家/买家、商品、订单。"""
import pytest

import config
from utils.api_client import ApiClient
from utils.data_factory import new_item, new_user


@pytest.fixture
def client():
    """未登录的 API 客户端。"""
    return ApiClient(config.BASE_URL)


@pytest.fixture
def logged_user():
    """注册并登录一个新用户，返回 dict：{client, user}。"""
    client = ApiClient(config.BASE_URL)
    user = new_user()
    client.register_and_login(user)
    return {"client": client, "user": user}


@pytest.fixture
def admin_client():
    """管理员客户端（种子数据 admin/123456）。"""
    client = ApiClient(config.BASE_URL)
    r = client.login(config.ADMIN["username"], config.ADMIN["password"])
    assert r.code == 200, "管理员登录失败: %s" % r
    return client


@pytest.fixture
def buyer():
    """买家：注册并登录一个新用户。"""
    client = ApiClient(config.BASE_URL)
    user = new_user()
    client.register_and_login(user)
    return {"client": client, "user": user}


@pytest.fixture
def seller():
    """卖家：注册并登录一个新用户。"""
    client = ApiClient(config.BASE_URL)
    user = new_user()
    client.register_and_login(user)
    return {"client": client, "user": user}


@pytest.fixture
def seller_item(seller):
    """卖家发布一个商品，返回 dict：{seller, item_id}。"""
    r = seller["client"].post("/api/items", json=new_item())
    assert r.code == 200, "发布商品失败: %s" % r
    return {"seller": seller, "item_id": r.body["id"]}


@pytest.fixture
def order(seller_item, buyer):
    """买家对卖家商品下单，返回 dict：{seller, buyer, item_id, order_id}。"""
    r = buyer["client"].post(
        "/api/orders",
        json={"itemId": seller_item["item_id"], "message": "自动化下单", "meetPlace": "图书馆门口"},
    )
    assert r.code == 200, "下单失败: %s" % r
    return {
        "seller": seller_item["seller"],
        "buyer": buyer,
        "item_id": seller_item["item_id"],
        "order_id": r.body["id"],
    }
