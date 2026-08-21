# -*- coding: utf-8 -*-
"""全局配置：服务地址、默认账号、超时等。"""

BASE_URL = "http://localhost:8080"

# 种子数据管理员账号（来自 campus_bazaar.sql，密码 123456）
ADMIN = {"username": "admin", "password": "123456"}

# 注册新用户的默认密码
USER_PASSWORD = "123456"

# 请求超时（秒）
REQUEST_TIMEOUT = 10
