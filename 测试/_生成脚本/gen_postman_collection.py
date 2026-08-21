# -*- coding: utf-8 -*-
"""
生成 Campus Bazaar Postman 接口测试集合（Collection v2.1）。
覆盖全部 34 个 REST 接口，每个接口含正常/异常/边界场景请求。
基于仓库真实 controller 定义生成；导入 Postman 后替换 {{baseUrl}} 即可运行。
运行：python gen_postman_collection.py → 输出 campus_bazaar.postman_collection.json
"""
import json, os

BASE = "{{baseUrl}}"
FOLDERS = []

def req(name, method, path, body=None, query=None, auth="公开", tests=True):
    """构造一个 Postman 请求对象。path 形如 "/api/items/{id}"。"""
    raw = BASE + path
    qs = []
    if query:
        for k, v in query:
            raw += ("&" if "?" in raw else "?") + k + "=" + str(v)
            qs.append({"key": k, "value": str(v), "description": ""})
    url = {"raw": raw, "host": [BASE]}
    url["path"] = path.split("/")
    hdrs = [{"key": "Content-Type", "value": "application/json", "type": "text"}]
    b = None
    if body is not None:
        b = {"mode": "raw", "raw": json.dumps(body, ensure_ascii=False, indent=2),
             "options": {"raw": {"language": "json"}}}
    event = []
    if tests:
        # 通用断言：HTTP 200 + 业务 code==0
        event.append({"listen": "test",
                      "script": {"type": "text/javascript",
                                 "exec": ["pm.test(\"状态码为200\", function () {",
                                          "    pm.response.to.have.status(200);",
                                          "});",
                                          "pm.test(\"业务code为0\", function () {",
                                          "    var json = pm.response.json();",
                                          "    pm.expect(json.code).to.eql(0);",
                                          "});"]}})
    return {"name": name,
            "event": event,
            "request": {"method": method, "header": hdrs,
                        "url": url,
                        "description": "场景类型与覆盖点见请求名；%s。" % ("需登录" if auth == "需登录" else "公开接口"),
                        "body": b}}

def add_folder(name, requests):
    FOLDERS.append({"name": name, "item": requests})

# ============================================================
# 01 用户模块
# ============================================================
u = []
u.append(req("[正常] 注册成功", "POST", "/api/users/register",
             {"username": "test01", "password": "123456", "nickname": "测试用户",
              "phone": "13900000001", "school": "XX大学"}, auth="公开"))
u.append(req("[异常] 用户名重复注册", "POST", "/api/users/register",
             {"username": "zhangsan", "password": "123456", "nickname": "张三重复",
              "phone": "13900000002", "school": "XX大学"}, auth="公开"))
u.append(req("[边界] 密码长度6位（合法边界）", "POST", "/api/users/register",
             {"username": "test02", "password": "123456", "nickname": "边界用户"}, auth="公开"))
u.append(req("[边界] 密码长度5位（非法）", "POST", "/api/users/register",
             {"username": "test03", "password": "12345", "nickname": "短密码用户"}, auth="公开"))
u.append(req("[边界] 用户名31字符超长", "POST", "/api/users/register",
             {"username": "u" * 31, "password": "123456", "nickname": "长用户名"}, auth="公开"))
u.append(req("[异常] 手机号10位格式错误", "POST", "/api/users/register",
             {"username": "test04", "password": "123456", "nickname": "手机号用户",
              "phone": "1390000000"}, auth="公开"))
u.append(req("[异常] 手机号含字母", "POST", "/api/users/register",
             {"username": "test05", "password": "123456", "nickname": "手机号字母",
              "phone": "1390000000a"}, auth="公开"))
u.append(req("[边界] 学校名称超长", "POST", "/api/users/register",
             {"username": "test06", "password": "123456", "nickname": "学校超长",
              "school": "学" * 51}, auth="公开"))
u.append(req("[正常] 登录成功", "POST", "/api/users/login",
             {"username": "zhangsan", "password": "123456"}, auth="公开"))
u.append(req("[异常] 登录密码错误", "POST", "/api/users/login",
             {"username": "zhangsan", "password": "wrong"}, auth="公开"))
u.append(req("[异常] 登录用户名不存在", "POST", "/api/users/login",
             {"username": "nobody", "password": "123456"}, auth="公开"))
u.append(req("[边界] 登录空密码", "POST", "/api/users/login",
             {"username": "zhangsan", "password": ""}, auth="公开"))
u.append(req("[异常] 禁用用户登录", "POST", "/api/users/login",
             {"username": "disabled_user", "password": "123456"}, auth="公开"))
u.append(req("[正常] 退出登录", "POST", "/api/users/logout", {}, auth="需登录"))
u.append(req("[边界] 未登录退出", "POST", "/api/users/logout", {}, auth="需登录"))
u.append(req("[正常] 获取当前登录用户", "GET", "/api/users/me", auth="需登录"))
u.append(req("[异常] 未登录获取个人信息", "GET", "/api/users/me", auth="需登录"))
u.append(req("[正常] 获取指定用户公开信息", "GET", "/api/users/1", auth="公开"))
u.append(req("[异常] 获取不存在用户", "GET", "/api/users/9999", auth="公开"))
u.append(req("[正常] 修改个人信息", "PUT", "/api/users/me",
             {"nickname": "新昵称", "phone": "13800001111", "school": "XX大学"}, auth="需登录"))
u.append(req("[异常] 修改非法手机号", "PUT", "/api/users/me", {"phone": "123"}, auth="需登录"))
u.append(req("[边界] 修改头像URL超长", "PUT", "/api/users/me",
             {"avatar": "https://example.com/" + "a" * 255}, auth="需登录"))
u.append(req("[正常] 查看我的收藏列表", "GET", "/api/users/me/favorites", auth="需登录"))
u.append(req("[异常] 未登录查看收藏", "GET", "/api/users/me/favorites", auth="需登录"))
add_folder("01_用户模块", u)

# ============================================================
# 02 商品模块
# ============================================================
i = []
i.append(req("[正常] 默认分页商品列表", "GET", "/api/items",
             query=[("pageNum", 1), ("pageSize", 10)], auth="公开"))
i.append(req("[正常] 按分类筛选", "GET", "/api/items", query=[("categoryId", 1)], auth="公开"))
i.append(req("[正常] 关键词搜索", "GET", "/api/items", query=[("keyword", "教材")], auth="公开"))
i.append(req("[正常] 价格升序", "GET", "/api/items", query=[("orderBy", "price_asc")], auth="公开"))
i.append(req("[正常] 价格降序", "GET", "/api/items", query=[("orderBy", "price_desc")], auth="公开"))
i.append(req("[正常] 组合筛选+分页", "GET", "/api/items",
             query=[("categoryId", 2), ("keyword", "教材"), ("pageNum", 1), ("pageSize", 5)], auth="公开"))
i.append(req("[边界] 分页越界", "GET", "/api/items", query=[("pageNum", 9999)], auth="公开"))
i.append(req("[边界] pageSize=1", "GET", "/api/items", query=[("pageSize", 1)], auth="公开"))
i.append(req("[边界] pageSize=1000超上限", "GET", "/api/items", query=[("pageSize", 1000)], auth="公开"))
i.append(req("[异常] 分类ID不存在", "GET", "/api/items", query=[("categoryId", 9999)], auth="公开"))
i.append(req("[正常] 空关键词搜索", "GET", "/api/items", query=[("keyword", "")], auth="公开"))
i.append(req("[正常] 商品详情", "GET", "/api/items/1", auth="公开"))
i.append(req("[异常] 商品详情不存在", "GET", "/api/items/9999", auth="公开"))
i.append(req("[边界] 商品ID为0", "GET", "/api/items/0", auth="公开"))
i.append(req("[正常] 发布商品", "POST", "/api/items",
             {"title": "测试发布-九成新台灯", "categoryId": 5, "price": 45.00,
              "original_price": 99.00, "condition_level": 2,
              "description": "功能正常，明盘出售", "images": ""}, auth="需登录"))
i.append(req("[异常] 未登录发布商品", "POST", "/api/items",
             {"title": "未登录发布", "categoryId": 1, "price": 10}, auth="需登录"))
i.append(req("[异常] 发布标题为空", "POST", "/api/items",
             {"title": "", "categoryId": 1, "price": 10}, auth="需登录"))
i.append(req("[边界] 发布标题50字符边界", "POST", "/api/items",
             {"title": "标" * 50, "categoryId": 1, "price": 10}, auth="需登录"))
i.append(req("[异常] 发布价格=0", "POST", "/api/items",
             {"title": "零价商品", "categoryId": 1, "price": 0}, auth="需登录"))
i.append(req("[异常] 发布价格=负数", "POST", "/api/items",
             {"title": "负价商品", "categoryId": 1, "price": -5}, auth="需登录"))
i.append(req("[边界] 价格小数精度12.999", "POST", "/api/items",
             {"title": "价格精度", "categoryId": 1, "price": 12.999}, auth="需登录"))
i.append(req("[异常] 发布分类不存在", "POST", "/api/items",
             {"title": "坏分类", "categoryId": 999, "price": 10}, auth="需登录"))
i.append(req("[异常] 发布成色非法", "POST", "/api/items",
             {"title": "坏成色", "categoryId": 1, "price": 10, "condition_level": 9}, auth="需登录"))
i.append(req("[正常] 卖家修改商品", "PUT", "/api/items/6",
             {"title": "修改后的标题", "price": 50.00}, auth="需登录"))
i.append(req("[异常] 非卖家修改他人商品", "PUT", "/api/items/1",
             {"title": "越权修改", "price": 1.00}, auth="需登录"))
i.append(req("[异常] 未登录修改商品", "PUT", "/api/items/6",
             {"title": "未登录改", "price": 1}, auth="需登录"))
i.append(req("[异常] 修改标题为空", "PUT", "/api/items/6", {"title": ""}, auth="需登录"))
i.append(req("[异常] 修改价格为负", "PUT", "/api/items/6", {"price": -1}, auth="需登录"))
i.append(req("[正常] 卖家下架商品", "DELETE", "/api/items/6", auth="需登录"))
i.append(req("[异常] 非卖家下架他人商品", "DELETE", "/api/items/1", auth="需登录"))
i.append(req("[异常] 未登录下架商品", "DELETE", "/api/items/6", auth="需登录"))
i.append(req("[异常] 交易中商品下架", "DELETE", "/api/items/7", auth="需登录"))
i.append(req("[正常] 收藏商品", "POST", "/api/items/1/favorite", auth="需登录"))
i.append(req("[异常] 未登录收藏", "POST", "/api/items/1/favorite", auth="需登录"))
i.append(req("[异常] 收藏不存在商品", "POST", "/api/items/9999/favorite", auth="需登录"))
i.append(req("[边界] 重复收藏同一商品", "POST", "/api/items/1/favorite", auth="需登录"))
i.append(req("[正常] 取消收藏", "DELETE", "/api/items/1/favorite", auth="需登录"))
i.append(req("[异常] 未登录取消收藏", "DELETE", "/api/items/1/favorite", auth="需登录"))
i.append(req("[边界] 取消未收藏商品", "DELETE", "/api/items/2/favorite", auth="需登录"))
i.append(req("[正常] 查看卖家商品列表", "GET", "/api/items/seller/2", auth="公开"))
i.append(req("[异常] 查看不存在卖家商品", "GET", "/api/items/seller/9999", auth="公开"))
i.append(req("[正常] 查看卖家在售商品", "GET", "/api/items/seller/2/onsale", auth="公开"))
i.append(req("[数据] 在售接口仅返回status=1", "GET", "/api/items/seller/2/onsale", auth="公开"))
add_folder("02_商品模块", i)

# ============================================================
# 03 分类模块
# ============================================================
c = []
c.append(req("[正常] 获取全部分类", "GET", "/api/categories", auth="公开"))
c.append(req("[正常] 未登录可访问分类", "GET", "/api/categories", auth="公开"))
c.append(req("[数据] 分类数量与种子数据一致", "GET", "/api/categories", auth="公开"))
add_folder("03_分类模块", c)

# ============================================================
# 04 订单模块
# ============================================================
o = []
o.append(req("[正常] 提交订单", "POST", "/api/orders",
             {"itemId": 1, "message": "食堂门口交易", "meetPlace": "第一食堂门口"}, auth="需登录"))
o.append(req("[异常] 未登录下单", "POST", "/api/orders",
             {"itemId": 1, "message": "", "meetPlace": ""}, auth="需登录"))
o.append(req("[异常] 下单不存在的商品", "POST", "/api/orders",
             {"itemId": 9999, "message": "", "meetPlace": ""}, auth="需登录"))
o.append(req("[异常] 自买自卖", "POST", "/api/orders",
             {"itemId": 1, "message": "", "meetPlace": ""}, auth="需登录"))
o.append(req("[异常] 下单已锁定商品", "POST", "/api/orders",
             {"itemId": 7, "message": "", "meetPlace": ""}, auth="需登录"))
o.append(req("[异常] 下单已售商品", "POST", "/api/orders",
             {"itemId": 8, "message": "", "meetPlace": ""}, auth="需登录"))
o.append(req("[异常] 下单待审核商品", "POST", "/api/orders",
             {"itemId": 9, "message": "", "meetPlace": ""}, auth="需登录"))
o.append(req("[异常] 请求体缺itemId", "POST", "/api/orders",
             {"message": "", "meetPlace": ""}, auth="需登录"))
o.append(req("[边界] 下单留言超长", "POST", "/api/orders",
             {"itemId": 1, "message": "留" * 201, "meetPlace": ""}, auth="需登录"))
o.append(req("[边界] 交易地点超长", "POST", "/api/orders",
             {"itemId": 1, "message": "", "meetPlace": "地" * 101}, auth="需登录"))
o.append(req("[正常] 我买到的订单", "GET", "/api/orders/buy", auth="需登录"))
o.append(req("[异常] 未登录查看买到订单", "GET", "/api/orders/buy", auth="需登录"))
o.append(req("[正常] 我卖出的订单", "GET", "/api/orders/sell", auth="需登录"))
o.append(req("[异常] 未登录查看卖出订单", "GET", "/api/orders/sell", auth="需登录"))
o.append(req("[正常] 卖家确认订单", "PUT", "/api/orders/4/confirm", auth="需登录"))
o.append(req("[异常] 买家确认订单", "PUT", "/api/orders/4/confirm", auth="需登录"))
o.append(req("[异常] 无关用户确认订单", "PUT", "/api/orders/4/confirm", auth="需登录"))
o.append(req("[异常] 确认已取消订单", "PUT", "/api/orders/5/confirm", auth="需登录"))
o.append(req("[异常] 未登录确认订单", "PUT", "/api/orders/4/confirm", auth="需登录"))
o.append(req("[正常] 买家确认完成交易", "PUT", "/api/orders/4/finish", auth="需登录"))
o.append(req("[异常] 卖家确认完成", "PUT", "/api/orders/4/finish", auth="需登录"))
o.append(req("[异常] 未确认订单直接完成", "PUT", "/api/orders/6/finish", auth="需登录"))
o.append(req("[异常] 未登录完成交易", "PUT", "/api/orders/4/finish", auth="需登录"))
o.append(req("[正常] 买家取消订单", "PUT", "/api/orders/6/cancel", auth="需登录"))
o.append(req("[正常] 卖家取消订单", "PUT", "/api/orders/6/cancel", auth="需登录"))
o.append(req("[异常] 已完成订单取消", "PUT", "/api/orders/4/cancel", auth="需登录"))
o.append(req("[异常] 未登录取消订单", "PUT", "/api/orders/6/cancel", auth="需登录"))
o.append(req("[正常] 卖家查看商品订单", "GET", "/api/orders/item/1", auth="需登录"))
o.append(req("[正常] 买家查看商品订单", "GET", "/api/orders/item/1", auth="需登录"))
o.append(req("[异常] 无关用户查看商品订单", "GET", "/api/orders/item/1", auth="需登录"))
o.append(req("[异常] 未登录查看商品订单", "GET", "/api/orders/item/1", auth="需登录"))
add_folder("04_订单模块", o)

# ============================================================
# 05 留言模块
# ============================================================
m = []
m.append(req("[正常] 获取商品留言列表", "GET", "/api/comments/item/1", auth="公开"))
m.append(req("[正常] 未登录查看留言", "GET", "/api/comments/item/1", auth="公开"))
m.append(req("[异常] 留言商品不存在", "GET", "/api/comments/item/9999", auth="公开"))
m.append(req("[正常] 发表留言", "POST", "/api/comments",
             {"itemId": 1, "content": "请问还在吗？"}, auth="需登录"))
m.append(req("[异常] 未登录留言", "POST", "/api/comments",
             {"itemId": 1, "content": "未登录留言"}, auth="需登录"))
m.append(req("[异常] 留言内容为空", "POST", "/api/comments",
             {"itemId": 1, "content": ""}, auth="需登录"))
m.append(req("[边界] 留言内容超长", "POST", "/api/comments",
             {"itemId": 1, "content": "留" * 201}, auth="需登录"))
m.append(req("[异常] 对不存在商品留言", "POST", "/api/comments",
             {"itemId": 9999, "content": "测试"}, auth="需登录"))
m.append(req("[正常] 回复留言", "POST", "/api/comments/1/reply", {"content": "还在的"}, auth="需登录"))
m.append(req("[异常] 未登录回复", "POST", "/api/comments/1/reply", {"content": "未登录"}, auth="需登录"))
m.append(req("[异常] 回复不存在留言", "POST", "/api/comments/9999/reply", {"content": "x"}, auth="需登录"))
m.append(req("[边界] 回复内容超长", "POST", "/api/comments/1/reply",
             {"content": "回" * 201}, auth="需登录"))
add_folder("05_留言模块", m)

# ============================================================
# 06 评价模块
# ============================================================
r = []
r.append(req("[正常] 获取商品评价", "GET", "/api/reviews/item/1", auth="公开"))
r.append(req("[正常] 无评价商品返回空", "GET", "/api/reviews/item/2", auth="公开"))
r.append(req("[正常] 未登录查看评价", "GET", "/api/reviews/item/1", auth="公开"))
r.append(req("[正常] 已完成订单可评价 check=true", "GET", "/api/reviews/check/4", auth="需登录"))
r.append(req("[正常] 未完成订单不可评价 check=false", "GET", "/api/reviews/check/6", auth="需登录"))
r.append(req("[异常] 未登录检查评价资格", "GET", "/api/reviews/check/4", auth="需登录"))
r.append(req("[正常] 提交5分评价", "POST", "/api/reviews",
             {"orderId": 4, "score": 5, "content": "交易顺利，推荐"}, auth="需登录"))
r.append(req("[正常] 提交1分评价", "POST", "/api/reviews",
             {"orderId": 4, "score": 1, "content": "体验一般"}, auth="需登录"))
r.append(req("[异常] 未登录提交评价", "POST", "/api/reviews",
             {"orderId": 4, "score": 5, "content": ""}, auth="需登录"))
r.append(req("[异常] 评分0越界", "POST", "/api/reviews",
             {"orderId": 4, "score": 0, "content": ""}, auth="需登录"))
r.append(req("[异常] 评分6越界", "POST", "/api/reviews",
             {"orderId": 4, "score": 6, "content": ""}, auth="需登录"))
r.append(req("[异常] 缺评分", "POST", "/api/reviews",
             {"orderId": 4, "content": ""}, auth="需登录"))
r.append(req("[异常] 一单一评重复评价", "POST", "/api/reviews",
             {"orderId": 4, "score": 3, "content": "重复评价"}, auth="需登录"))
r.append(req("[异常] 对不存在订单评价", "POST", "/api/reviews",
             {"orderId": 9999, "score": 3, "content": ""}, auth="需登录"))
r.append(req("[边界] 评价内容超长", "POST", "/api/reviews",
             {"orderId": 4, "score": 3, "content": "评" * 301}, auth="需登录"))
add_folder("06_评价模块", r)

# ============================================================
# 07 管理后台
# ============================================================
a = []
a.append(req("[正常] 管理员用户列表", "GET", "/api/admin/users",
             query=[("page", 1), ("size", 10)], auth="需登录"))
a.append(req("[异常] 普通用户访问管理接口", "GET", "/api/admin/users",
             query=[("page", 1), ("size", 10)], auth="需登录"))
a.append(req("[异常] 未登录访问管理接口", "GET", "/api/admin/users", auth="需登录"))
a.append(req("[边界] 用户列表分页越界", "GET", "/api/admin/users",
             query=[("page", 9999), ("size", 10)], auth="需登录"))
a.append(req("[正常] 禁用用户", "PUT", "/api/admin/users/4/status", {"status": 0}, auth="需登录"))
a.append(req("[正常] 启用用户", "PUT", "/api/admin/users/4/status", {"status": 1}, auth="需登录"))
a.append(req("[异常] 禁用不存在用户", "PUT", "/api/admin/users/9999/status", {"status": 0}, auth="需登录"))
a.append(req("[异常] 用户状态非法值", "PUT", "/api/admin/users/4/status", {"status": 9}, auth="需登录"))
a.append(req("[正常] 管理端商品列表", "GET", "/api/admin/items",
             query=[("page", 1), ("size", 10)], auth="需登录"))
a.append(req("[正常] 按状态筛选商品", "GET", "/api/admin/items",
             query=[("status", 0)], auth="需登录"))
a.append(req("[正常] 按关键词搜索商品", "GET", "/api/admin/items",
             query=[("keyword", "教材")], auth="需登录"))
a.append(req("[正常] 审核通过商品", "PUT", "/api/admin/items/9/status", {"status": 1}, auth="需登录"))
a.append(req("[正常] 管理员下架商品", "PUT", "/api/admin/items/10/status", {"status": 4}, auth="需登录"))
a.append(req("[异常] 商品状态非法值", "PUT", "/api/admin/items/9/status", {"status": 9}, auth="需登录"))
a.append(req("[异常] 修改不存在商品状态", "PUT", "/api/admin/items/9999/status", {"status": 1}, auth="需登录"))
add_folder("07_管理后台", a)

# ============================================================
# 组装集合
# ============================================================
total = sum(len(f["item"]) for f in FOLDERS)
collection = {
    "info": {
        "name": "Campus Bazaar 接口测试集合",
        "description": ("校园二手集市接口测试集合。覆盖全部接口的正常/异常/边界场景。\n"
                        "使用方式：\n"
                        "1) 启动后端(mvn spring-boot:run)与MySQL；\n"
                        "2) 新建环境 baseUrl = http://localhost:8080；\n"
                        "3) 登录类接口需先运行「登录成功」请求获得Cookie（Postman自动保存）；\n"
                        "4) 运行集合或单请求，测试断言校验 code==0。"),
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "variable": [{"key": "baseUrl", "value": "http://localhost:8080", "type": "string"}],
    "item": FOLDERS,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "02_接口测试",
                   "campus_bazaar.postman_collection.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(collection, f, ensure_ascii=False, indent=2)
print("生成完成：共 %d 个请求 -> %s" % (total, out))
for fd in FOLDERS:
    print("  %s: %d 个请求" % (fd["name"], len(fd["item"])))
