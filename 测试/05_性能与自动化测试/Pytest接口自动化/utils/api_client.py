# -*- coding: utf-8 -*-
"""基于 requests.Session 的轻量 API 客户端。
Session 自动维持登录 Cookie，模拟真实浏览器会话。
"""
import requests

import config


class ApiResponse:
    """统一封装的响应对象。"""
    def __init__(self, http_status, data):
        self.status = http_status              # HTTP 状态码
        self.data = data or {}                 # 解析后的 JSON
        self.code = self.data.get("code")      # 业务码（200 成功，400/401/403/404/500 失败）
        self.message = self.data.get("message")
        self.body = self.data.get("data")

    @property
    def ok(self):
        return self.status == 200 and self.code == 200

    def __repr__(self):
        return "<ApiResponse status=%s code=%s message=%s>" % (
            self.status, self.code, self.message)


class ApiClient:
    def __init__(self, base_url=None):
        self.base_url = (base_url or config.BASE_URL).rstrip("/")
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", config.REQUEST_TIMEOUT)
        resp = self.session.request(method, self.base_url + path, **kwargs)
        try:
            payload = resp.json()
        except ValueError:
            payload = {"code": resp.status_code, "message": resp.text, "data": None}
        return ApiResponse(resp.status_code, payload)

    def get(self, path, params=None):
        return self.request("GET", path, params=params)

    def post(self, path, json=None):
        return self.request("POST", path, json=json)

    def put(self, path, json=None):
        return self.request("PUT", path, json=json)

    def delete(self, path):
        return self.request("DELETE", path)

    # ---- 便捷登录 ----
    def login(self, username, password):
        return self.post("/api/users/login", json={"username": username, "password": password})

    def register_and_login(self, user):
        r = self.post("/api/users/register", json=user)
        assert r.code == 200, "注册失败: %s" % r
        r = self.login(user["username"], user["password"])
        assert r.code == 200, "登录失败: %s" % r
        return r.body
