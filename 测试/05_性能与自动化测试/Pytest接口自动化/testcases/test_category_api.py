# -*- coding: utf-8 -*-
"""分类模块接口自动化用例。"""
import pytest

from utils import assertions

pytestmark = pytest.mark.regression


def test_get_categories_success(client):
    """正常：获取全部分类 → 成功且数量>=5（种子数据）。"""
    r = client.get("/api/categories")
    assertions.assert_success(r)
    assert isinstance(r.body, list)
    assert len(r.body) >= 5, "分类数量异常: %d" % len(r.body)


def test_category_fields_complete(client):
    """数据：分类字段含 id/name/icon/sort。"""
    r = client.get("/api/categories")
    assertions.assert_success(r)
    for c in r.body:
        assert "id" in c and "name" in c and "icon" in c and "sort" in c


def test_categories_public_without_login(client):
    """公开性：未登录可访问分类接口。"""
    r = client.get("/api/categories")
    assertions.assert_success(r)
