# -*- coding: utf-8 -*-
"""评价模块接口自动化用例（一单一评/评分边界/资格校验）。"""
import pytest

from utils import assertions

pytestmark = pytest.mark.regression


def test_can_review_and_create_after_finish(order):
    """正常：交易完成后买家可评价。"""
    seller = order["seller"]["client"]
    buyer = order["buyer"]["client"]
    assertions.assert_success(seller.put("/api/orders/%s/confirm" % order["order_id"]))
    assertions.assert_success(buyer.put("/api/orders/%s/finish" % order["order_id"]))

    check = buyer.get("/api/reviews/check/%s" % order["order_id"])
    assertions.assert_success(check)
    assert check.body is True, "交易完成后应可评价"

    r = buyer.post("/api/reviews",
                   json={"orderId": order["order_id"], "score": 5, "content": "交易顺利，推荐"})
    assertions.assert_success(r)


def test_cannot_review_before_finish(order):
    """异常：订单未完成不可评价。"""
    buyer = order["buyer"]["client"]
    check = buyer.get("/api/reviews/check/%s" % order["order_id"])
    assertions.assert_success(check)
    assert check.body is False, "未完成交易不应可评价"

    r = buyer.post("/api/reviews", json={"orderId": order["order_id"], "score": 5, "content": ""})
    assertions.assert_biz_error(r, 400, "无法评价该订单")


def test_review_score_out_of_range(order):
    """边界：评分越界(0/6) → 400。"""
    buyer = order["buyer"]["client"]
    r = buyer.post("/api/reviews", json={"orderId": order["order_id"], "score": 0, "content": ""})
    assertions.assert_biz_error(r, 400, "评分必须在1-5之间")


def test_duplicate_review_rejected(order):
    """异常：一单一评，重复评价 → 400。"""
    seller = order["seller"]["client"]
    buyer = order["buyer"]["client"]
    assertions.assert_success(seller.put("/api/orders/%s/confirm" % order["order_id"]))
    assertions.assert_success(buyer.put("/api/orders/%s/finish" % order["order_id"]))
    assertions.assert_success(
        buyer.post("/api/reviews", json={"orderId": order["order_id"], "score": 4, "content": "第一次评价"}))
    r = buyer.post("/api/reviews", json={"orderId": order["order_id"], "score": 3, "content": "重复评价"})
    assertions.assert_biz_error(r, 400, "无法评价该订单")


def test_get_review_by_item_after_review(order):
    """功能：评价后可通过商品查询到评价。"""
    seller = order["seller"]["client"]
    buyer = order["buyer"]["client"]
    assertions.assert_success(seller.put("/api/orders/%s/confirm" % order["order_id"]))
    assertions.assert_success(buyer.put("/api/orders/%s/finish" % order["order_id"]))
    assertions.assert_success(
        buyer.post("/api/reviews", json={"orderId": order["order_id"], "score": 5, "content": "很棒"}))
    r = buyer.get("/api/reviews/item/%s" % order["item_id"])
    assertions.assert_success(r)
    assert r.body is not None, "评价后应能查到商品评价"
