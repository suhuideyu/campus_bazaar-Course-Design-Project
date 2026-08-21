# -*- coding: utf-8 -*-
"""订单模块接口自动化用例（下单/确认/完成/取消/双视角）。"""
import pytest

from utils import assertions
from utils.api_client import ApiClient
from utils.data_factory import new_order, new_user

pytestmark = pytest.mark.regression


def test_submit_order_locks_item(order, seller_item):
    """正常：买家下单成功，商品锁定为待确认订单。"""
    # order fixture 已断言下单成功；此处校验商品状态联动
    seller = order["seller"]["client"]
    r = seller.get("/api/items/%s" % order["item_id"])
    assertions.assert_success(r)
    assert r.body["status"] == 2, "下单后商品应锁定(status=2)"


def test_submit_order_own_item(seller_item):
    """异常：卖家购买自己的商品 → 400。"""
    seller = seller_item["seller"]
    r = seller["client"].post("/api/orders", json=new_order(seller_item["item_id"]))
    assertions.assert_biz_error(r, 400, "不能购买自己发布的商品")


def test_submit_order_on_locked_item(order):
    """异常：商品已锁定后他人再下单 → 400。"""
    other = ApiClient()
    other.register_and_login(new_user())
    r = other.post("/api/orders", json=new_order(order["item_id"]))
    assertions.assert_biz_error(r, 400, "不可购买")


def test_submit_order_item_not_found(buyer):
    """异常：商品不存在 → 404。"""
    r = buyer["client"].post("/api/orders", json=new_order(999999))
    assertions.assert_biz_error(r, 404, "商品不存在")


def test_submit_order_requires_login(client):
    """安全：未登录下单 → 401。"""
    r = client.post("/api/orders", json=new_order(1))
    assertions.assert_biz_error(r, 401, "请先登录")


def test_confirm_order_by_seller(order):
    """正常：卖家确认订单，状态置为已确认。"""
    seller = order["seller"]["client"]
    assertions.assert_success(seller.put("/api/orders/%s/confirm" % order["order_id"]))


def test_confirm_order_by_buyer_forbidden(order):
    """安全：买家确认订单 → 403。"""
    buyer = order["buyer"]["client"]
    r = buyer.put("/api/orders/%s/confirm" % order["order_id"])
    assertions.assert_biz_error(r, 403, "无权")


def test_finish_order_by_buyer_success(order):
    """正常：买家确认完成交易，商品已售且卖家信用+2。"""
    seller = order["seller"]
    buyer = order["buyer"]
    assertions.assert_success(seller["client"].put("/api/orders/%s/confirm" % order["order_id"]))
    assertions.assert_success(buyer["client"].put("/api/orders/%s/finish" % order["order_id"]))

    r = seller["client"].get("/api/items/%s" % order["item_id"])
    assertions.assert_success(r)
    assert r.body["status"] == 3, "交易完成后商品应为已售(status=3)"

    me = seller["client"].get("/api/users/me")
    assertions.assert_success(me)
    assert me.body["creditScore"] == 102, "卖家信用分应+2"


def test_finish_order_before_confirm(order):
    """异常：未确认订单直接完成 → 400。"""
    r = order["buyer"]["client"].put("/api/orders/%s/finish" % order["order_id"])
    assertions.assert_biz_error(r, 400, "尚未被卖家确认")


def test_cancel_order_by_buyer_unlocks_item(order):
    """正常：买家取消订单，商品恢复在售。"""
    assertions.assert_success(
        order["buyer"]["client"].put("/api/orders/%s/cancel" % order["order_id"])
    )
    r = order["seller"]["client"].get("/api/items/%s" % order["item_id"])
    assertions.assert_success(r)
    assert r.body["status"] == 1, "取消订单后商品应恢复在售(status=1)"


def test_cancel_finished_order(order):
    """异常：已完成订单不可取消 → 400。"""
    seller = order["seller"]["client"]
    buyer = order["buyer"]["client"]
    assertions.assert_success(seller.put("/api/orders/%s/confirm" % order["order_id"]))
    assertions.assert_success(buyer.put("/api/orders/%s/finish" % order["order_id"]))
    r = buyer.put("/api/orders/%s/cancel" % order["order_id"])
    assertions.assert_biz_error(r, 400, "无法再次取消")


def test_get_order_by_item_visibility(order):
    """数据：商品订单仅买卖双方可见，无关用户返回 null。"""
    item_id = order["item_id"]
    # 卖家可见
    assertions.assert_success(order["seller"]["client"].get("/api/orders/item/%s" % item_id))
    # 买家可见
    assertions.assert_success(order["buyer"]["client"].get("/api/orders/item/%s" % item_id))
    # 无关用户 data 为 null
    other = ApiClient()
    other.register_and_login(new_user())
    r = other.get("/api/orders/item/%s" % item_id)
    assertions.assert_success(r)
    assert r.body is None, "无关用户不应看到该商品订单"
