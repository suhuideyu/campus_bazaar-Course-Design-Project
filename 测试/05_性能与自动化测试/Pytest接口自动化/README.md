# Campus Bazaar 接口自动化测试框架

基于 **Python + Requests + Pytest** 的接口自动化测试框架，覆盖校园二手集市全部核心业务流程。

## 一、框架结构

```
Pytest接口自动化/
├── config.py                 # 全局配置（服务地址/管理员账号/超时）
├── conftest.py               # 全局 fixtures（客户端/用户/买家/卖家/商品/订单）
├── pytest.ini                # pytest 配置
├── requirements.txt          # 依赖
├── utils/
│   ├── api_client.py         # ApiClient：基于 requests.Session，自动维持登录态
│   ├── data_factory.py       # 测试数据工厂（唯一用户名/商品/订单数据）
│   └── assertions.py         # 公共断言（成功/业务错误码/密码脱敏）
├── testcases/                # 用例（7 个模块，共 50 条）
│   ├── test_user_api.py      # 用户模块 8 条
│   ├── test_category_api.py  # 分类模块 3 条
│   ├── test_item_api.py      # 商品模块 12 条
│   ├── test_order_api.py     # 订单模块 12 条（含完整交易流转）
│   ├── test_comment_api.py   # 留言模块 6 条
│   ├── test_review_api.py    # 评价模块 5 条（一单一评）
│   └── test_admin_api.py     # 管理后台 4 条
└── reports/                  # 测试报告输出目录（运行时生成）
```

## 二、环境准备

```bash
# 1. 启动数据库与后端
#    MySQL 导入 campus_bazaar.sql；cd campus-bazaar-boot && mvn spring-boot:run
# 2. 安装依赖
pip install -r requirements.txt
```

## 三、运行方式

```bash
# 全部用例
pytest

# 指定模块
pytest testcases/test_user_api.py

# 并行执行（需 pytest-xdist）
pytest -n auto

# 生成 HTML 报告（需 pytest-html）
pytest --html=reports/report.html --self-contained-html

# 失败用例自动重跑（需 pytest-rerunfailures）
pytest --reruns 1

# 冒烟标记用例
pytest -m smoke
```

## 四、用例设计要点

| 覆盖维度 | 说明 | 示例 |
|----------|------|------|
| 正常主流程 | 下单→确认→完成→评价 全链路 | `test_finish_order_by_buyer_success` |
| 业务规则 | 自买自卖/一单一评/交易中不可下架 | `test_confirm_order_by_buyer_forbidden` |
| 权限与安全 | 未登录401/越权403/管理隔离 | `test_normal_user_forbidden_admin` |
| 数据一致性 | 商品锁定/已售状态联动、信用分联动 | `test_cancel_order_by_buyer_unlocks_item` |
| 边界与异常 | 空值/超长/越界评分/不存在资源 | `test_review_score_out_of_range` |

## 五、数据隔离策略

- 每次运行使用**唯一用户名/手机号**注册全新用户，测试数据互不干扰；
- 订单类用例通过 fixture 现场创建"卖家发布→买家下单"的独立数据链；
- 管理后台用例复用种子数据 `admin/123456`。

## 六、与回归套件的关系

本框架中的用例全部标记 `regression`，构成**核心流程回归套件**：
单模块定位用 `pytest testcases/xx.py`，全量回归用 `pytest -n auto`，
配合 pytest-xdist 并行与数据隔离，是回归效率优化的主要实现手段
（详见 `../回归效率优化对比报告.md`）。
