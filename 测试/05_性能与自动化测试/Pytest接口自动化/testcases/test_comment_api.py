# -*- coding: utf-8 -*-
"""留言模块接口自动化用例（留言/回复/列表）。"""
import pytest

from utils import assertions

pytestmark = pytest.mark.regression


def test_list_comments_public(client):
    """公开性：未登录可查看商品留言列表。"""
    r = client.get("/api/comments/item/1")
    assertions.assert_success(r)


def test_add_comment_success(logged_user):
    """正常：登录用户发表留言。"""
    r = logged_user["client"].post("/api/comments", json={"itemId": 1, "content": "请问还在吗？"})
    assertions.assert_success(r)


def test_add_comment_requires_login(client):
    """安全：未登录留言 → 401。"""
    r = client.post("/api/comments", json={"itemId": 1, "content": "未登录留言"})
    assertions.assert_biz_error(r, 401, "请先登录")


def test_add_comment_empty_content(logged_user):
    """异常：留言内容为空 → 400。"""
    r = logged_user["client"].post("/api/comments", json={"itemId": 1, "content": ""})
    assertions.assert_biz_error(r, 400, "留言内容不能为空")


def test_add_comment_too_long(logged_user):
    """边界：留言内容超过200字 → 400。"""
    r = logged_user["client"].post("/api/comments",
                                   json={"itemId": 1, "content": "留" * 201})
    assertions.assert_biz_error(r, 400, "不能超过200字")


def test_reply_comment_success(logged_user):
    """正常：回复留言，reply_id 指向父留言。"""
    c = logged_user["client"]
    cid = c.post("/api/comments", json={"itemId": 1, "content": "根留言"}).body["id"]
    r = c.post("/api/comments/%s/reply" % cid, json={"content": "回复内容"})
    assertions.assert_success(r)
    assert r.body["replyId"] == cid, "回复应指向父留言"
