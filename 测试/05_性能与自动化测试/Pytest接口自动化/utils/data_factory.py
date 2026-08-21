# -*- coding: utf-8 -*-
"""测试数据工厂：生成唯一用户名/手机号与默认商品、订单数据。"""
import random
import string
import time


def unique_suffix():
    return "%d%d" % (int(time.time()), random.randint(1000, 9999))


def unique_username(prefix="tester"):
    return "%s_%s" % (prefix, unique_suffix())


def new_user(**overrides):
    """生成一个可注册的新用户 JSON。"""
    suffix = unique_suffix()
    user = {
        "username": "auto_%s" % suffix,
        "password": "123456",
        "nickname": "自动化_%s" % suffix[-4:],
        "phone": "139" + "".join(random.choices(string.digits, k=8)),
        "school": "测试大学",
    }
    user.update(overrides)
    return user


def new_item(**overrides):
    """生成一个可发布的商品 JSON（camelCase 与后端 Item 字段一致）。"""
    item = {
        "title": "自动化测试商品_%s" % unique_suffix(),
        "categoryId": 1,
        "price": 66.66,
        "originalPrice": 99.00,
        "conditionLevel": 3,
        "description": "接口自动化测试发布，功能正常",
        "images": "",
    }
    item.update(overrides)
    return item


def new_order(item_id, **overrides):
    order = {"itemId": item_id, "message": "自动化测试下单", "meetPlace": "图书馆门口"}
    order.update(overrides)
    return order
