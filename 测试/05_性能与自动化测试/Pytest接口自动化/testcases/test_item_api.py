# -*- coding: utf-8 -*-
"""商品模块接口自动化用例（列表/详情/发布/修改/下架/收藏）。"""
import pytest

from utils import assertions
from utils.data_factory import new_item, new_user

pytestmark = pytest.mark.regression


def test_list_items_success(client):
    """正常：默认分页商品列表。"""
    r = client.get("/api/items", params={"pageNum": 1, "pageSize": 10})
    assertions.assert_success(r)
    assert "list" in r.body or isinstance(r.body, dict), "分页结果结构异常"


def test_list_items_filter_by_category(client):
    """正常：按分类筛选。"""
    r = client.get("/api/items", params={"categoryId": 1})
    assertions.assert_success(r)


def test_list_items_search_keyword(client):
    """正常：关键词搜索（无匹配返回空列表，业务码仍为200）。"""
    r = client.get("/api/items", params={"keyword": "不存在的关键词xyz"})
    assertions.assert_success(r)


def test_item_detail_view_count_increment(client):
    """功能：浏览详情浏览量自增。"""
    r1 = client.get("/api/items/1")
    assertions.assert_success(r1)
    r2 = client.get("/api/items/1")
    assertions.assert_success(r2)
    assert r2.body["viewCount"] == r1.body["viewCount"] + 1, "viewCount 未自增"


def test_item_detail_not_found(client):
    """异常：商品不存在 → 404。"""
    r = client.get("/api/items/999999")
    assertions.assert_biz_error(r, 404, "商品不存在")


def test_publish_item_success(logged_user):
    """正常：发布商品成功，状态为待审核(0)。"""
    c = logged_user["client"]
    r = c.post("/api/items", json=new_item())
    assertions.assert_success(r)
    assert r.body["id"] is not None
    assert r.body["status"] == 0, "新发布商品状态应为待审核"


def test_publish_item_empty_title(logged_user):
    """异常：标题为空 → 400。"""
    r = logged_user["client"].post("/api/items", json=new_item(title=""))
    assertions.assert_biz_error(r, 400, "商品标题不能为空")


def test_publish_item_negative_price(logged_user):
    """异常：价格<=0 → 400。"""
    r = logged_user["client"].post("/api/items", json=new_item(price=-1))
    assertions.assert_biz_error(r, 400, "价格必须大于 0")


def test_update_item_by_seller(logged_user):
    """正常：卖家本人修改商品。"""
    c = logged_user["client"]
    item_id = c.post("/api/items", json=new_item()).body["id"]
    r = c.put("/api/items/%s" % item_id, json={"title": "修改后标题", "price": 88.88})
    assertions.assert_success(r)


def test_update_item_by_other_user(logged_user, client):
    """安全：非卖家修改他人商品 → 403。"""
    seller = logged_user["client"]
    item_id = seller.post("/api/items", json=new_item()).body["id"]
    other = client
    other.register_and_login(new_user())
    r = other.put("/api/items/%s" % item_id, json={"title": "越权修改"})
    assertions.assert_biz_error(r, 403, "无权")


def test_update_item_requires_login(client):
    """安全：未登录修改商品 → 401。"""
    r = client.put("/api/items/1", json={"title": "未登录修改"})
    assertions.assert_biz_error(r, 401, "请先登录")


def test_take_down_item_by_seller(logged_user):
    """正常：卖家下架商品，状态置为4。"""
    c = logged_user["client"]
    item_id = c.post("/api/items", json=new_item()).body["id"]
    assertions.assert_success(c.delete("/api/items/%s" % item_id))
    r = c.get("/api/items/%s" % item_id)
    assertions.assert_success(r)
    assert r.body["status"] == 4, "下架后商品状态应为4"
