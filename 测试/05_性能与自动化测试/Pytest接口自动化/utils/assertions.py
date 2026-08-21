# -*- coding: utf-8 -*-
"""公共断言工具。"""


def assert_success(resp, msg=None):
    """断言业务成功：HTTP 200 且 code==200。"""
    assert resp.status == 200, "HTTP状态码异常: %s %s" % (resp.status, msg or "")
    assert resp.code == 200, "业务码异常 code=%s, message=%s, %s" % (resp.code, resp.message, msg or "")


def assert_biz_error(resp, code, msg_contains=None):
    """断言业务失败并校验错误码与错误消息。"""
    assert resp.code == code, "期望业务码=%s，实际 code=%s message=%s" % (code, resp.code, resp.message)
    if msg_contains:
        assert msg_contains in (resp.message or ""), (
            "期望消息包含[%s]，实际[%s]" % (msg_contains, resp.message))


def assert_no_password(resp):
    """断言响应不包含明文密码字段。"""
    body = resp.body
    if isinstance(body, dict):
        assert "password" not in body, "响应不应包含 password 字段"
