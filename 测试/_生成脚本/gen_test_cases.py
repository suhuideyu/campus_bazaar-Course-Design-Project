# -*- coding: utf-8 -*-
"""
生成 Campus Bazaar 测试用例库 CSV。
用例内容基于仓库真实接口（controller）与数据库表结构（campus_bazaar.sql）编写。
列：用例ID, 业务模块, 优先级, 用例类型, 用例标题, 前置条件, 测试步骤, 预期结果, 关联接口
运行：python gen_test_cases.py   → 输出 220条测试用例.csv
"""
import csv, os

# 用例格式：(业务模块, 优先级, 用例类型, 用例标题, 前置条件, 测试步骤, 预期结果, 关联接口)
CASES = []

def add(mod, prio, ctype, title, pre, steps, expected, api):
    CASES.append((mod, prio, ctype, title, pre, steps, expected, api))

# ============================================================
# 一、用户模块（36）
# ============================================================
U = "用户模块"
add(U, "P0", "功能", "正常注册成功", "数据库无同名用户", "1.打开注册页 2.输入合法username/password/nickname 3.提交", "注册成功，提示『注册成功』，数据库新增用户记录", "POST /api/users/register")
add(U, "P0", "异常", "用户名重复注册", "已存在用户 zhangsan", "1.用 zhangsan 作为用户名注册 2.提交", "注册失败，提示用户名已存在，不产生新记录", "POST /api/users/register")
add(U, "P0", "异常", "密码长度校验", "注册页可输入", "1.输入长度小于6位的密码 2.提交", "注册失败或提示密码长度不足", "POST /api/users/register")
add(U, "P1", "边界", "用户名超长", "注册页可输入", "1.输入超过30字符的用户名 2.提交", "注册失败，提示用户名超长", "POST /api/users/register")
add(U, "P1", "异常", "用户名含非法字符", "注册页可输入", "1.输入含空格/特殊符号的用户名 2.提交", "注册失败或用户名被裁剪，不允许非法字符入库", "POST /api/users/register")
add(U, "P1", "功能", "注册昵称必填", "注册页可输入", "1.不填昵称只填其余字段 2.提交", "注册失败，提示昵称不能为空", "POST /api/users/register")
add(U, "P2", "边界", "手机号格式校验", "注册页可输入", "1.输入10位或含字母的手机号 2.提交", "注册失败，提示手机号格式错误（需11位数字）", "POST /api/users/register")
add(U, "P2", "边界", "学校字段超长", "注册页可输入", "1.输入超过50字符的学校名 2.提交", "注册失败，提示学校名超长", "POST /api/users/register")
add(U, "P0", "功能", "正常登录", "已注册用户 zhangsan/123456", "1.输入正确用户名密码 2.登录", "登录成功，返回用户信息且不含password字段", "POST /api/users/login")
add(U, "P0", "异常", "密码错误登录", "已注册用户", "1.输入正确用户名+错误密码 2.登录", "登录失败，提示用户名或密码错误", "POST /api/users/login")
add(U, "P0", "异常", "用户名不存在登录", "无该用户", "1.输入不存在的用户名 2.登录", "登录失败，提示用户名或密码错误", "POST /api/users/login")
add(U, "P0", "异常", "空参数登录", "登录页", "1.用户名或密码为空 2.登录", "登录失败，不产生空值查询异常", "POST /api/users/login")
add(U, "P0", "异常", "已禁用用户登录", "存在status=0被禁用用户", "1.用被禁用用户登录", "登录失败，提示账号已被禁用", "POST /api/users/login")
add(U, "P1", "安全", "登录态保持", "登录成功", "1.登录后携带Cookie/Session访问需登录接口", "请求成功，说明Session登录态生效", "GET /api/users/me")
add(U, "P1", "功能", "密码大小写敏感", "注册时密码含大小写", "1.登录时输入大小写不一致的密码", "登录失败，密码区分大小写", "POST /api/users/login")
add(U, "P1", "功能", "正常登出", "已登录用户", "1.调用登出接口 2.再访问需登录接口", "登出成功，之后访问需登录接口被拦截", "POST /api/users/logout")
add(U, "P2", "边界", "未登录登出", "未登录状态", "1.直接调用登出接口", "接口幂等返回成功，不抛异常", "POST /api/users/logout")
add(U, "P0", "功能", "获取当前登录用户信息", "已登录用户", "1.调用 /me", "返回当前用户信息，不含password", "GET /api/users/me")
add(U, "P0", "安全", "未登录访问个人信息", "未登录", "1.调用 /me", "请求被拦截，返回未登录错误", "GET /api/users/me")
add(U, "P0", "功能", "正常修改个人信息", "已登录用户", "1.修改昵称/头像/手机号/学校 2.提交", "修改成功，重新查询个人信息为新值", "PUT /api/users/me")
add(U, "P1", "异常", "修改非法手机号", "已登录用户", "1.将手机号改为10位 2.提交", "修改失败，提示手机号格式错误", "PUT /api/users/me")
add(U, "P2", "边界", "头像URL超长", "已登录用户", "1.输入超过255字符的URL 2.提交", "修改失败，提示头像URL超长", "PUT /api/users/me")
add(U, "P2", "异常", "修改登录用户名", "已登录用户", "1.尝试通过个人信息接口修改username", "修改被忽略或拒绝，用户名不可被普通修改", "PUT /api/users/me")
add(U, "P0", "功能", "获取指定用户公开信息", "存在目标用户", "1.调用 /api/users/{id}", "返回用户公开信息，不含password", "GET /api/users/{id}")
add(U, "P1", "异常", "获取不存在用户", "无该id用户", "1.调用 /api/users/{id}（不存在id）", "返回错误，提示用户不存在", "GET /api/users/{id}")
add(U, "P1", "安全", "公开信息不含密码字段", "任意用户", "1.调用 /api/users/{id} 检查返回字段", "响应JSON中不含password字段", "GET /api/users/{id}")
add(U, "P0", "功能", "查看我的收藏列表", "已登录且有收藏", "1.调用 /api/users/me/favorites", "返回当前用户收藏列表", "GET /api/users/me/favorites")
add(U, "P0", "安全", "未登录查看收藏", "未登录", "1.调用 /api/users/me/favorites", "请求被拦截，返回未登录错误", "GET /api/users/me/favorites")
add(U, "P1", "功能", "收藏列表按时间倒序", "已登录且有多条收藏", "1.查看收藏列表顺序", "列表按收藏时间倒序排列", "GET /api/users/me/favorites")
add(U, "P1", "安全", "密码加密存储", "数据库可查询", "1.查询 cb_user.password", "存储值为MD5密文（如e10adc...），非明文", "数据校验")
add(U, "P1", "安全", "会话过期后需登录接口被拦截", "Session过期/未登录", "1.访问需登录接口", "被拦截并提示未登录", "登录拦截器")
add(U, "P1", "安全", "普通用户访问管理接口被拦截", "普通用户已登录", "1.调用 /api/admin/users", "被管理员拦截器拒绝，提示无权限", "管理员拦截器")
add(U, "P1", "边界", "用户名前后空格处理", "注册页可输入", "1.用户名带前后空格注册", "用户名被trim或提示非法字符，不存带空格用户名", "POST /api/users/register")
add(U, "P2", "功能", "批量注册多个用户", "数据库无冲突", "1.依次注册多个不同用户名", "全部注册成功，用户名均唯一", "POST /api/users/register")
add(U, "P1", "数据", "用户名唯一索引", "数据库可查询", "1.检查 cb_user 唯一索引", "username 存在 UNIQUE 索引约束", "数据校验")
add(U, "P2", "功能", "注册后自动登录态", "注册页", "1.注册成功后访问需登录接口", "若设计为自动登录则放行，否则返回未登录", "POST /api/users/register")

# ============================================================
# 二、商品模块（50）
# ============================================================
I = "商品模块"
add(I, "P0", "功能", "默认分页商品列表", "系统有在售商品", "1.调用 GET /api/items", "返回分页结果，仅包含status=1在售商品", "GET /api/items")
add(I, "P0", "功能", "按分类筛选", "存在分类数据", "1.调用 GET /api/items?categoryId=1", "返回分类1下的在售商品", "GET /api/items")
add(I, "P0", "功能", "关键词搜索", "存在商品含关键词", "1.调用 GET /api/items?keyword=教材", "返回标题/描述含关键词的在售商品", "GET /api/items")
add(I, "P1", "功能", "价格升序排序", "存在多价格商品", "1.调用 GET /api/items?orderBy=price_asc", "返回结果按价格从小到大", "GET /api/items")
add(I, "P1", "功能", "价格降序排序", "存在多价格商品", "1.调用 GET /api/items?orderBy=price_desc", "返回结果按价格从大到小", "GET /api/items")
add(I, "P1", "功能", "按热度排序", "存在浏览量差异商品", "1.调用排序接口指定热度", "返回结果按view_count降序", "GET /api/items")
add(I, "P1", "边界", "分页越界", "商品总数有限", "1.调用 pageNum 远大于总页数", "返回空列表，不报错", "GET /api/items")
add(I, "P1", "边界", "pageSize边界值", "系统有商品", "1.调用 pageSize=1 与 pageSize=1000", "pageSize=1返回1条；超限值被限制或按上限返回", "GET /api/items")
add(I, "P1", "功能", "搜索无结果", "关键词无匹配", "1.调用 GET /api/items?keyword=不存在的词", "返回空列表，提示正常", "GET /api/items")
add(I, "P0", "数据", "列表仅含在售商品", "存在待审核/下架/已售商品", "1.调用列表接口检查返回", "列表不含待审核、下架、已售、锁定商品", "GET /api/items")
add(I, "P2", "边界", "分类ID不存在", "无该分类", "1.调用 GET /api/items?categoryId=999", "返回空列表，不报错", "GET /api/items")
add(I, "P0", "功能", "正常获取商品详情", "存在在售商品", "1.调用 GET /api/items/{id}", "返回商品完整信息", "GET /api/items/{id}")
add(I, "P1", "功能", "浏览详情浏览量+1", "存在商品", "1.记录view_count 2.访问详情 3.再查询", "view_count 增加1", "GET /api/items/{id}")
add(I, "P0", "异常", "获取不存在商品", "无该id商品", "1.调用 GET /api/items/{id}（不存在）", "返回错误，提示商品不存在", "GET /api/items/{id}")
add(I, "P1", "数据", "已下架商品详情不可见", "存在下架商品", "1.访问下架商品详情", "返回错误或提示商品不可见", "GET /api/items/{id}")
add(I, "P1", "功能", "详情价格两位小数", "存在商品", "1.检查详情返回的price", "价格以两位小数返回（DECIMAL(10,2)）", "GET /api/items/{id}")
add(I, "P0", "功能", "正常发布商品", "已登录卖家", "1.填写合法商品信息发布", "发布成功，商品进入待审核(status=0)", "POST /api/items")
add(I, "P0", "安全", "未登录发布商品", "未登录", "1.调用发布接口", "被拦截，返回未登录错误", "POST /api/items")
add(I, "P0", "异常", "发布标题为空", "已登录卖家", "1.不填标题发布", "发布失败，提示标题不能为空", "POST /api/items")
add(I, "P0", "边界", "发布标题超长", "已登录卖家", "1.输入超过50字符标题发布", "发布失败，提示标题超长", "POST /api/items")
add(I, "P0", "异常", "发布价格为0或负数", "已登录卖家", "1.输入price=0或-1发布", "发布失败，价格必须大于0", "POST /api/items")
add(I, "P1", "边界", "价格小数精度", "已登录卖家", "1.输入 price=12.999 发布", "价格按两位小数处理（12.99/12.00）", "POST /api/items")
add(I, "P0", "异常", "发布分类不存在", "已登录卖家", "1.填写不存在的categoryId发布", "发布失败，提示分类不存在", "POST /api/items")
add(I, "P2", "边界", "描述超长", "已登录卖家", "1.输入超长描述发布", "TEXT字段接受，若前端限长则提示", "POST /api/items")
add(I, "P1", "边界", "图片URL超长", "已登录卖家", "1.输入超过500字符images发布", "发布失败，提示图片链接超长", "POST /api/items")
add(I, "P1", "异常", "成色非法值", "已登录卖家", "1.输入condition_level=0或6", "发布失败，成色取值1-5", "POST /api/items")
add(I, "P1", "功能", "发布后状态为待审核", "已登录卖家", "1.发布商品 2.查询商品状态", "商品status=0待审核", "POST /api/items")
add(I, "P0", "数据", "待审核商品不在公开列表", "已发布待审核商品", "1.调用商品列表接口", "待审核商品不出现", "GET /api/items")
add(I, "P0", "功能", "卖家本人修改商品", "已登录卖家本人", "1.修改本人商品标题/价格", "修改成功，重新查询为新值", "PUT /api/items/{id}")
add(I, "P0", "安全", "非卖家修改他人商品", "已登录普通用户", "1.调用修改接口改他人商品", "被拒绝，提示无权限", "PUT /api/items/{id}")
add(I, "P0", "安全", "未登录修改商品", "未登录", "1.调用修改接口", "被拦截，返回未登录错误", "PUT /api/items/{id}")
add(I, "P0", "异常", "修改标题为空", "已登录卖家", "1.将标题清空提交修改", "修改失败，提示标题不能为空", "PUT /api/items/{id}")
add(I, "P1", "异常", "修改价格为负", "已登录卖家", "1.将价格改为负数提交", "修改失败，价格必须大于0", "PUT /api/items/{id}")
add(I, "P1", "异常", "修改锁定/已售商品", "商品已锁定或已售", "1.卖家修改交易中商品", "修改被拒绝，交易中商品不可改", "PUT /api/items/{id}")
add(I, "P0", "功能", "卖家本人下架商品", "已登录卖家本人", "1.调用下架接口", "商品下架成功，status=4", "DELETE /api/items/{id}")
add(I, "P0", "安全", "下架他人商品", "已登录普通用户", "1.调用下架接口下架他人商品", "被拒绝，提示无权限", "DELETE /api/items/{id}")
add(I, "P0", "异常", "交易中商品不可下架", "商品已锁定/已售", "1.卖家对交易中商品调用下架", "下架被拒绝", "DELETE /api/items/{id}")
add(I, "P0", "数据", "下架后公开列表不可见", "已下架商品", "1.调用商品列表/详情", "下架商品不再出现", "GET /api/items")
add(I, "P0", "安全", "未登录下架商品", "未登录", "1.调用下架接口", "被拦截，返回未登录错误", "DELETE /api/items/{id}")
add(I, "P0", "功能", "登录后收藏商品", "已登录用户+在售商品", "1.调用收藏接口", "收藏成功，提示收藏成功", "POST /api/items/{id}/favorite")
add(I, "P1", "功能", "重复收藏同一商品", "已收藏该商品", "1.再次调用收藏接口", "幂等处理，不产生重复收藏记录", "POST /api/items/{id}/favorite")
add(I, "P0", "安全", "未登录收藏商品", "未登录", "1.调用收藏接口", "被拦截，返回未登录错误", "POST /api/items/{id}/favorite")
add(I, "P1", "异常", "收藏不存在商品", "无该商品", "1.调用收藏接口收藏不存在商品", "收藏失败，提示商品不存在", "POST /api/items/{id}/favorite")
add(I, "P0", "功能", "取消收藏", "已收藏该商品", "1.调用取消收藏接口", "取消成功，收藏记录删除", "DELETE /api/items/{id}/favorite")
add(I, "P1", "功能", "取消未收藏商品", "未收藏该商品", "1.调用取消收藏接口", "幂等处理，返回成功", "DELETE /api/items/{id}/favorite")
add(I, "P0", "安全", "未登录取消收藏", "未登录", "1.调用取消收藏接口", "被拦截，返回未登录错误", "DELETE /api/items/{id}/favorite")
add(I, "P1", "功能", "查看卖家商品列表", "存在卖家商品", "1.调用 GET /api/items/seller/{sellerId}", "返回该卖家全部商品", "GET /api/items/seller/{sellerId}")
add(I, "P0", "数据", "查看卖家在售商品", "卖家存在多状态商品", "1.调用 GET /api/items/seller/{sellerId}/onsale", "仅返回status=1在售商品", "GET /api/items/seller/{sellerId}/onsale")
add(I, "P2", "边界", "不存在卖家的商品列表", "无该卖家", "1.调用 GET /api/items/seller/{sellerId}（不存在）", "返回空列表，不报错", "GET /api/items/seller/{sellerId}")
add(I, "P1", "功能", "商品状态流转：发布到在售", "商品待审核", "1.管理员审核通过 2.查看商品", "商品状态由0变为1，公开可见", "PUT /api/admin/items/{id}/status")

# ============================================================
# 三、分类模块（10）
# ============================================================
C = "分类模块"
add(C, "P0", "功能", "获取全部分类", "系统有分类数据", "1.调用 GET /api/categories", "返回全部分类列表", "GET /api/categories")
add(C, "P1", "功能", "分类字段完整性", "系统有分类", "1.检查返回的分类字段", "含 id/name/icon/sort 字段", "GET /api/categories")
add(C, "P1", "数据", "分类数量与种子数据一致", "初始数据库", "1.查询分类数量", "与初始化数据一致（5条）", "GET /api/categories")
add(C, "P1", "功能", "分类排序", "系统有分类", "1.检查返回顺序", "按 sort 权重排序", "GET /api/categories")
add(C, "P1", "数据", "分类名唯一约束", "数据库可查询", "1.检查 cb_category.name", "存在 UNIQUE 约束", "数据校验")
add(C, "P2", "边界", "无分类数据", "清空分类表", "1.调用分类接口", "返回空列表，不报错", "GET /api/categories")
add(C, "P1", "功能", "分类接口公开访问", "未登录", "1.调用分类接口", "无需登录即可访问", "GET /api/categories")
add(C, "P1", "功能", "统一响应格式", "系统有分类", "1.检查响应结构", "返回 {code,msg,data} 标准结构", "GET /api/categories")
add(C, "P1", "数据", "分类名长度限制", "数据库可查询", "1.检查 cb_category.name 字段长度", "name 长度 ≤20", "数据校验")
add(C, "P2", "功能", "新增分类后列表可见", "管理员可新增分类（数据层）", "1.插入新分类 2.调用列表接口", "新分类实时出现在列表", "GET /api/categories")

# ============================================================
# 四、订单模块（46）
# ============================================================
O = "订单模块"
add(O, "P0", "功能", "正常下单", "已登录买家+在售商品", "1.调用提交订单接口", "订单创建成功status=0待确认，商品锁定(status=2)", "POST /api/orders")
add(O, "P0", "安全", "未登录下单", "未登录", "1.调用提交订单接口", "被拦截，返回未登录错误", "POST /api/orders")
add(O, "P0", "异常", "下单不存在的商品", "无该商品", "1.对不存在itemId下单", "下单失败，提示商品不存在", "POST /api/orders")
add(O, "P0", "异常", "自买自卖", "买家=商品卖家", "1.对自己发布的商品下单", "下单失败，不能购买自己的商品", "POST /api/orders")
add(O, "P0", "异常", "重复下单已锁定商品", "商品已锁定(status=2)", "1.对已锁定商品下单", "下单失败，提示商品已被预订", "POST /api/orders")
add(O, "P0", "异常", "下单已售/下架商品", "商品status=3或4", "1.对已售/下架商品下单", "下单失败，商品不可购买", "POST /api/orders")
add(O, "P0", "异常", "下单待审核商品", "商品status=0", "1.对待审核商品下单", "下单失败，商品不可购买", "POST /api/orders")
add(O, "P1", "异常", "不传itemId下单", "已登录买家", "1.提交无itemId的请求体", "返回参数错误(400/提示)", "POST /api/orders")
add(O, "P1", "边界", "留言超长", "已登录买家", "1.提交超过200字符message", "下单失败或message被截断", "POST /api/orders")
add(O, "P2", "边界", "交易地点超长", "已登录买家", "1.提交超过100字符meetPlace", "下单失败或meetPlace被截断", "POST /api/orders")
add(O, "P0", "数据", "订单号唯一且格式正确", "下单成功", "1.检查返回的orderNo", "orderNo唯一且以ORD开头", "POST /api/orders")
add(O, "P1", "数据", "订单价格取商品当前价格", "商品价格已知", "1.下单后检查订单price", "订单price与商品price一致", "POST /api/orders")
add(O, "P0", "功能", "买家可见下单记录", "买家已下单", "1.调用 GET /api/orders/buy", "返回买家订单列表，含新订单", "GET /api/orders/buy")
add(O, "P0", "功能", "卖家可见新订单", "卖家有商品被下单", "1.调用 GET /api/orders/sell", "返回卖家订单列表，含新订单", "GET /api/orders/sell")
add(O, "P0", "功能", "卖家确认订单", "订单status=0待确认", "1.卖家调用确认接口", "订单status=1已确认，confirmed_at被记录", "PUT /api/orders/{id}/confirm")
add(O, "P0", "安全", "买家确认订单", "订单待确认", "1.买家调用确认接口", "被拒绝，只有卖家可确认", "PUT /api/orders/{id}/confirm")
add(O, "P0", "安全", "非交易双方确认订单", "无关用户", "1.无关用户调用确认接口", "被拒绝，提示无权限", "PUT /api/orders/{id}/confirm")
add(O, "P1", "异常", "确认已取消订单", "订单status=3已取消", "1.卖家调用确认接口", "操作失败，订单已取消", "PUT /api/orders/{id}/confirm")
add(O, "P0", "安全", "未登录确认订单", "未登录", "1.调用确认接口", "被拦截，返回未登录错误", "PUT /api/orders/{id}/confirm")
add(O, "P0", "功能", "买家确认完成交易", "订单status=1已确认", "1.买家调用完成接口", "订单status=2已完成，商品转为已售(status=3)", "PUT /api/orders/{id}/finish")
add(O, "P0", "安全", "卖家调用完成接口", "订单已确认", "1.卖家调用完成接口", "被拒绝，只有买家可完成", "PUT /api/orders/{id}/finish")
add(O, "P0", "异常", "未确认订单直接完成", "订单status=0", "1.买家调用完成接口", "操作失败，订单未确认", "PUT /api/orders/{id}/finish")
add(O, "P0", "数据", "完成后商品转已售", "交易完成", "1.检查商品状态", "商品status=3已售", "PUT /api/orders/{id}/finish")
add(O, "P0", "功能", "买家取消待确认订单", "订单status=0", "1.买家调用取消接口", "订单status=3已取消，商品解锁回在售", "PUT /api/orders/{id}/cancel")
add(O, "P0", "功能", "卖家取消订单", "订单待确认/已确认", "1.卖家调用取消接口", "订单取消成功", "PUT /api/orders/{id}/cancel")
add(O, "P0", "异常", "已完成订单不可取消", "订单status=2", "1.调用取消接口", "操作失败，订单已完成", "PUT /api/orders/{id}/cancel")
add(O, "P0", "数据", "取消后商品恢复在售", "订单已取消", "1.检查商品状态", "商品status=1在售", "PUT /api/orders/{id}/cancel")
add(O, "P0", "数据", "取消后商品可被他人下单", "订单已取消", "1.他人对同商品下单", "下单成功", "POST /api/orders")
add(O, "P1", "功能", "卖家查看商品订单", "卖家有商品被下单", "1.调用 GET /api/orders/item/{itemId}", "返回该商品关联订单", "GET /api/orders/item/{itemId}")
add(O, "P1", "功能", "买家查看商品订单", "买家有订单", "1.调用 GET /api/orders/item/{itemId}", "返回该商品关联订单", "GET /api/orders/item/{itemId}")
add(O, "P0", "安全", "无关用户查看商品订单", "无关用户", "1.调用 GET /api/orders/item/{itemId}", "被拒绝，仅买卖双方可查看", "GET /api/orders/item/{itemId}")
add(O, "P0", "安全", "未登录查看商品订单", "未登录", "1.调用 GET /api/orders/item/{itemId}", "被拦截，返回未登录错误", "GET /api/orders/item/{itemId}")
add(O, "P0", "功能", "我买到的订单列表", "买家有订单", "1.调用 GET /api/orders/buy", "返回买家视角订单", "GET /api/orders/buy")
add(O, "P0", "功能", "我卖出的订单列表", "卖家有订单", "1.调用 GET /api/orders/sell", "返回卖家视角订单", "GET /api/orders/sell")
add(O, "P0", "数据", "买卖双视角数据隔离", "存在多个用户订单", "1.对比A的buy与B的sell", "双方只能看到与自己相关的订单", "GET /api/orders/buy|sell")
add(O, "P1", "功能", "订单列表字段完整", "存在订单", "1.检查订单列表字段", "含订单号/商品/价格/状态/时间等关键字段", "GET /api/orders/buy")
add(O, "P1", "功能", "订单状态合法流转", "订单待确认", "1.按 待确认→已确认→已完成 流转", "状态依次 0→1→2 正常流转", "PUT /api/orders/{id}")
add(O, "P1", "异常", "非法状态跳转", "订单待确认", "1.直接调用完成接口(跳过确认)", "操作失败，禁止跳步", "PUT /api/orders/{id}/finish")
add(O, "P1", "数据", "订单状态与商品状态联动", "交易中", "1.对比订单状态与商品状态", "订单锁定对应商品锁定，完成对应已售", "数据校验")
add(O, "P1", "数据", "并发下单仅一单成功", "同一在售商品", "1.两用户并发下单", "仅一人下单成功，另一人提示已被预订", "POST /api/orders")
add(O, "P1", "数据", "订单价格与商品价格一致", "数据库可查询", "1.执行关联校验SQL", "订单price=商品price", "数据校验")
add(O, "P1", "数据", "订单卖家与商品卖家一致", "数据库可查询", "1.执行关联校验SQL", "订单seller_id=商品seller_id", "数据校验")
add(O, "P1", "数据", "买卖双方不同", "数据库可查询", "1.执行校验SQL", "订单buyer_id≠seller_id", "数据校验")
add(O, "P1", "数据", "一单一评约束", "数据库可查询", "1.检查已完成订单评价", "每个已完成订单至多一条评价", "数据校验")
add(O, "P1", "数据", "订单号全局唯一", "数据库可查询", "1.检查 order_no 重复", "无重复订单号", "数据校验")
add(O, "P1", "数据", "取消订单无遗留锁定", "数据库可查询", "1.查询已取消订单对应商品状态", "商品已恢复在售，无遗留锁定", "数据校验")

# ============================================================
# 五、留言模块（20）
# ============================================================
M = "留言模块"
add(M, "P0", "功能", "正常留言", "已登录用户+在售商品", "1.调用留言接口", "留言成功，返回留言记录", "POST /api/comments")
add(M, "P0", "安全", "未登录留言", "未登录", "1.调用留言接口", "被拦截，返回未登录错误", "POST /api/comments")
add(M, "P0", "异常", "留言内容为空", "已登录用户", "1.提交空content", "留言失败，提示内容不能为空", "POST /api/comments")
add(M, "P1", "边界", "留言内容超长", "已登录用户", "1.提交超过200字符content", "留言失败，提示内容超长", "POST /api/comments")
add(M, "P0", "异常", "对不存在商品留言", "无该商品", "1.对不存在itemId留言", "留言失败，提示商品不存在", "POST /api/comments")
add(M, "P1", "功能", "留言列表按时间排序", "商品有多条留言", "1.调用留言列表接口", "留言按时间排序展示", "GET /api/comments/item/{itemId}")
add(M, "P1", "功能", "留言含用户信息", "存在留言", "1.检查留言列表返回", "含留言用户昵称/头像", "GET /api/comments/item/{itemId}")
add(M, "P2", "边界", "对已下架商品留言", "商品下架", "1.对下架商品留言", "按业务设计允许或拒绝", "POST /api/comments")
add(M, "P1", "数据", "根留言reply_id为空", "存在根留言", "1.检查根留言reply_id", "根留言reply_id为NULL", "GET /api/comments/item/{itemId}")
add(M, "P0", "功能", "正常回复留言", "存在根留言", "1.调用回复接口", "回复成功，reply_id指向父留言", "POST /api/comments/{id}/reply")
add(M, "P0", "异常", "回复不存在留言", "无该留言", "1.回复不存在的留言id", "回复失败，提示留言不存在", "POST /api/comments/{id}/reply")
add(M, "P0", "安全", "未登录回复", "未登录", "1.调用回复接口", "被拦截，返回未登录错误", "POST /api/comments/{id}/reply")
add(M, "P1", "功能", "嵌套回复", "存在一级回复", "1.对回复再回复", "支持嵌套回复，reply_id正确", "POST /api/comments/{id}/reply")
add(M, "P1", "边界", "回复内容超长", "存在根留言", "1.提交超长回复内容", "回复失败，提示内容超长", "POST /api/comments/{id}/reply")
add(M, "P1", "功能", "留言公开可见", "未登录", "1.调用留言列表接口", "无需登录即可查看留言", "GET /api/comments/item/{itemId}")
add(M, "P1", "功能", "多留言均可见", "商品有多条留言", "1.调用列表接口", "全部留言按序返回", "GET /api/comments/item/{itemId}")
add(M, "P1", "数据", "留言关联正确", "数据库可查询", "1.执行关联校验SQL", "comment.item_id 对应真实商品", "数据校验")
add(M, "P1", "数据", "留言时间字段正确", "留言成功", "1.检查返回的created_at", "created_at为当前时间", "POST /api/comments")
add(M, "P1", "数据", "留言用户存在性", "数据库可查询", "1.执行FK校验SQL", "comment.user_id 对应真实用户", "数据校验")
add(M, "P2", "数据", "留言内容长度约束", "数据库可查询", "1.检查 content 字段", "content VARCHAR(200)", "数据校验")

# ============================================================
# 六、评价模块（20）
# ============================================================
R = "评价模块"
add(R, "P0", "功能", "交易完成后可评价", "订单已完成", "1.调用检查接口 2.调用提交评价接口", "check返回true，评价成功", "GET /api/reviews/check/{orderId}")
add(R, "P0", "异常", "未完成交易不可评价", "订单未完成", "1.对待确认/已确认订单调用check", "check返回false，不可评价", "GET /api/reviews/check/{orderId}")
add(R, "P0", "安全", "非买家评价", "无关用户", "1.对他人订单提交评价", "被拒绝，仅买家可评价", "POST /api/reviews")
add(R, "P0", "安全", "未登录评价", "未登录", "1.调用提交评价接口", "被拦截，返回未登录错误", "POST /api/reviews")
add(R, "P1", "功能", "评分1-5合法", "订单已完成", "1.分别提交score=1/3/5", "评价成功，评分正确保存", "POST /api/reviews")
add(R, "P0", "异常", "评分越界", "订单已完成", "1.提交score=0/6", "评价失败，评分需1-5", "POST /api/reviews")
add(R, "P0", "异常", "评分缺失", "订单已完成", "1.不传score提交", "评价失败，提示评分不能为空", "POST /api/reviews")
add(R, "P1", "边界", "评价内容超长", "订单已完成", "1.提交超过300字符content", "评价失败，提示内容超长", "POST /api/reviews")
add(R, "P0", "异常", "一单一评重复评价", "订单已有评价", "1.对同一订单再次评价", "评价失败，一单一评", "POST /api/reviews")
add(R, "P1", "数据", "订单唯一评价约束", "数据库可查询", "1.检查 cb_review.order_id", "存在UNIQUE约束，一单一评", "数据校验")
add(R, "P0", "功能", "获取商品评价", "商品有评价", "1.调用 GET /api/reviews/item/{itemId}", "返回该商品评价", "GET /api/reviews/item/{itemId}")
add(R, "P1", "功能", "无评价商品返回空", "商品无评价", "1.调用获取评价接口", "返回空结果", "GET /api/reviews/item/{itemId}")
add(R, "P1", "功能", "评价公开可见", "未登录", "1.调用获取评价接口", "无需登录可查看评价", "GET /api/reviews/item/{itemId}")
add(R, "P1", "功能", "评价含评分与内容", "存在评价", "1.检查评价返回字段", "含score与content", "GET /api/reviews/item/{itemId}")
add(R, "P1", "数据", "评价双方正确", "数据库可查询", "1.检查reviewer/reviewee", "评价者为买家，被评价者为卖家", "数据校验")
add(R, "P1", "数据", "评分影响卖家信用分", "评价完成", "1.检查卖家credit_score", "信用分按评价联动更新", "数据校验")
add(R, "P1", "数据", "评价时间正确", "评价成功", "1.检查created_at", "为当前时间", "POST /api/reviews")
add(R, "P0", "异常", "对不存在订单评价", "无该订单", "1.对不存在orderId评价", "评价失败，提示订单不存在", "POST /api/reviews")
add(R, "P1", "异常", "已取消订单不可评价", "订单已取消", "1.对已取消订单提交评价", "评价失败", "POST /api/reviews")
add(R, "P1", "边界", "评价内容可选为空", "订单已完成", "1.不传content只传score", "评价成功，content为空可接受", "POST /api/reviews")

# ============================================================
# 七、收藏模块（18）
# ============================================================
F = "收藏模块"
add(F, "P0", "功能", "正常收藏", "已登录用户+在售商品", "1.调用收藏接口", "收藏成功", "POST /api/items/{id}/favorite")
add(F, "P0", "安全", "未登录收藏", "未登录", "1.调用收藏接口", "被拦截，返回未登录错误", "POST /api/items/{id}/favorite")
add(F, "P0", "异常", "收藏不存在商品", "无该商品", "1.收藏不存在商品", "收藏失败，提示商品不存在", "POST /api/items/{id}/favorite")
add(F, "P1", "数据", "重复收藏唯一约束", "数据库可查询", "1.检查 cb_favorite", "(user_id,item_id) 存在UNIQUE约束", "数据校验")
add(F, "P1", "功能", "收藏在售商品", "商品在售", "1.收藏在售商品", "收藏成功", "POST /api/items/{id}/favorite")
add(F, "P1", "边界", "收藏待审核/下架商品", "商品非在售", "1.收藏待审核/下架商品", "按业务设计允许或拒绝", "POST /api/items/{id}/favorite")
add(F, "P1", "功能", "收藏列表含商品信息", "已收藏", "1.查看收藏列表", "含商品信息", "GET /api/users/me/favorites")
add(F, "P1", "数据", "收藏后fav_count增加", "商品收藏数", "1.收藏后检查商品fav_count", "fav_count增加1", "POST /api/items/{id}/favorite")
add(F, "P1", "数据", "取消收藏后fav_count减少", "已收藏", "1.取消收藏后检查fav_count", "fav_count减少1", "DELETE /api/items/{id}/favorite")
add(F, "P1", "功能", "取消未收藏商品幂等", "未收藏", "1.取消收藏未收藏商品", "返回成功，不报错", "DELETE /api/items/{id}/favorite")
add(F, "P0", "安全", "未登录取消收藏", "未登录", "1.调用取消收藏接口", "被拦截，返回未登录错误", "DELETE /api/items/{id}/favorite")
add(F, "P1", "功能", "收藏列表时间倒序", "多条收藏", "1.查看收藏顺序", "按收藏时间倒序", "GET /api/users/me/favorites")
add(F, "P2", "边界", "收藏列表为空", "未收藏", "1.查看收藏列表", "返回空列表，不报错", "GET /api/users/me/favorites")
add(F, "P1", "数据", "收藏数据隔离", "多用户", "1.对比不同用户收藏", "仅返回当前用户收藏", "GET /api/users/me/favorites")
add(F, "P1", "数据", "收藏数与fav_count一致性", "数据库可查询", "1.执行聚合校验SQL", "收藏记录数与fav_count一致", "数据校验")
add(F, "P1", "功能", "收藏标记回显", "已收藏", "1.查看商品详情/列表", "已收藏商品正确标记", "GET /api/items/{id}")
add(F, "P1", "数据", "收藏用户存在性", "数据库可查询", "1.执行FK校验SQL", "收藏user_id对应真实用户", "数据校验")
add(F, "P1", "数据", "收藏商品存在性", "数据库可查询", "1.执行FK校验SQL", "收藏item_id对应真实商品", "数据校验")

# ============================================================
# 八、管理后台（20）
# ============================================================
A = "管理后台"
add(A, "P0", "功能", "管理员获取用户列表", "管理员登录", "1.调用 /api/admin/users", "返回分页用户列表", "GET /api/admin/users")
add(A, "P0", "安全", "普通用户访问管理接口", "普通用户登录", "1.调用 /api/admin/users", "被拦截，无权限", "GET /api/admin/users")
add(A, "P0", "安全", "未登录访问管理接口", "未登录", "1.调用 /api/admin/users", "被拦截，返回未登录错误", "GET /api/admin/users")
add(A, "P1", "功能", "用户列表分页", "存在多用户", "1.调用 page=1&size=10", "按分页返回", "GET /api/admin/users")
add(A, "P1", "边界", "用户列表分页越界", "用户总数有限", "1.调用 page 超范围", "返回空列表，不报错", "GET /api/admin/users")
add(A, "P0", "功能", "禁用用户", "存在正常用户", "1.调用状态修改接口 status=0", "用户status=0，提示已禁用", "PUT /api/admin/users/{id}/status")
add(A, "P0", "功能", "启用用户", "存在禁用用户", "1.调用状态修改接口 status=1", "用户status=1，提示已启用", "PUT /api/admin/users/{id}/status")
add(A, "P0", "数据", "禁用用户无法登录", "用户被禁用", "1.用禁用账号登录", "登录失败，提示账号已禁用", "POST /api/users/login")
add(A, "P1", "数据", "禁用后会话失效", "用户已禁用且在线", "1.被禁用后访问需登录接口", "请求被拦截", "登录拦截器")
add(A, "P1", "异常", "禁用不存在用户", "无该用户", "1.对不存在id修改状态", "操作失败，提示用户不存在", "PUT /api/admin/users/{id}/status")
add(A, "P0", "功能", "管理端查看商品列表", "管理员登录", "1.调用 /api/admin/items", "返回商品分页列表（含待审核）", "GET /api/admin/items")
add(A, "P1", "功能", "按状态筛选商品", "存在多状态商品", "1.调用 status=0", "仅返回待审核商品", "GET /api/admin/items")
add(A, "P1", "功能", "按关键词搜索商品", "存在匹配商品", "1.调用 keyword=教材", "返回匹配商品", "GET /api/admin/items")
add(A, "P0", "功能", "审核通过商品", "商品待审核", "1.调用状态修改接口 status=1", "商品status=1，公开可见", "PUT /api/admin/items/{id}/status")
add(A, "P0", "数据", "审核通过后公开可见", "商品已审核", "1.调用商品列表", "商品出现在公开列表", "GET /api/items")
add(A, "P0", "功能", "管理员下架商品", "商品在售", "1.调用状态修改接口 status=4", "商品status=4下架", "PUT /api/admin/items/{id}/status")
add(A, "P0", "数据", "下架后公开不可见", "商品已下架", "1.调用商品列表/详情", "下架商品不再出现", "GET /api/items")
add(A, "P1", "异常", "非法状态值", "存在商品", "1.提交status=9", "操作失败，状态值非法", "PUT /api/admin/items/{id}/status")
add(A, "P1", "异常", "修改不存在商品状态", "无该商品", "1.对不存在id修改状态", "操作失败，提示商品不存在", "PUT /api/admin/items/{id}/status")
add(A, "P1", "数据", "商品状态非法流转", "商品已售", "1.尝试将已售商品改回在售", "按业务规则拒绝或明确限制", "PUT /api/admin/items/{id}/status")

# ============================================================
# 写入 CSV
# ============================================================
assert len(CASES) == 220, "用例数量错误: %d" % len(CASES)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_功能与回归测试", "220条测试用例.csv")
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["用例ID", "业务模块", "优先级", "用例类型", "用例标题", "前置条件", "测试步骤", "预期结果", "关联接口"])
    for i, c in enumerate(CASES, 1):
        w.writerow(["CB_TC_%03d" % i] + list(c))

print("生成完成：共 %d 条用例 -> %s" % (len(CASES), out))

# 统计输出
from collections import Counter
mod = Counter(c[0] for c in CASES)
prio = Counter(c[1] for c in CASES)
ctype = Counter(c[2] for c in CASES)
print("模块分布:", dict(mod))
print("优先级分布:", dict(prio))
print("类型分布:", dict(ctype))
