# 🏫 校园二手集市 (Campus Bazaar)

一个面向高校在校生的闲置物品交易平台，支持商品发布浏览、在线交易、留言评价等核心功能。采用前后端分离架构，后端基于 Spring Boot + MyBatis，前端基于 Vue 3 + Vite。

---

## 功能一览

### 👤 用户端

| 功能 | 描述 |
|------|------|
| 注册 / 登录 | 用户名 + MD5 加密密码登录，Session 维持登录态 |
| 商品浏览 | 首页商品列表，支持分类筛选、关键词搜索、价格/热度排序、分页 |
| 商品详情 | 查看商品图文信息、卖家信息、留言与评价，浏览量自动 +1 |
| 发布商品 | 填写标题、描述、图片、价格、成色等，发布后进入待审核状态 |
| 编辑/下架商品 | 卖家本人可修改或下架自己的商品（交易中不可下架） |
| 收藏商品 | 收藏感兴趣的商品，在个人中心查看收藏列表 |
| 下单购买 | 提交订单（含留言与见面地点），商品自动锁定防重复购买 |
| 查看订单 | 「我买到的」和「我卖出的」双视角订单列表 |
| 确认交易 | 卖家确认订单 → 买家确认完成 / 取消订单（任一方均可取消） |
| 信用评价 | 交易完成后买家可对卖家进行 1-5 分评分+文字评价（一单一评） |
| 留言/回复 | 商品详情页留言，支持嵌套回复 |
| 个人信息管理 | 修改昵称、头像、手机号、学校等资料 |

### 🔧 管理后台

| 功能 | 描述 |
|------|------|
| 用户管理 | 查看所有用户列表，支持分页；启用/禁用账号 |
| 商品管理 | 查看所有商品列表，支持按状态筛选+关键词搜索；审核通过/下架商品 |

---

## 技术栈

### 后端

| 技术 | 用途 |
|------|------|
| **Java 8+** | 开发语言 |
| **Spring Boot 2.x** | 应用框架（IoC、事务、Web MVC） |
| **MyBatis** | 数据持久化（XML 映射 + 动态 SQL） |
| **MySQL 8.0** | 关系型数据库（UTF8MB4） |
| **Maven** | 项目构建与依赖管理 |
| **SLF4J** | 日志门面 |

### 前端

| 技术 | 用途 |
|------|------|
| **Vue 3** | 前端框架（Composition API） |
| **Vite** | 构建工具 |
| **Vue Router** | 前端路由（含登录守卫） |
| **Pinia** | 状态管理（用户登录态） |
| **Axios** | HTTP 请求封装 |
| **Element Plus** | UI 组件库 |

---

## 项目结构

```
campus-bazaar/
├── campus-bazaar-boot/                # 后端 Spring Boot 项目
│   ├── src/main/java/com/bazaar/
│   │   ├── CampusBazaarApplication.java      # 启动类
│   │   ├── common/Result.java                # 统一 JSON 响应体 {code, msg, data}
│   │   ├── config/WebMvcConfig.java          # Web 配置（CORS 跨域等）
│   │   ├── controller/                       # 控制器层（7 个，共 30+ 个 REST API）
│   │   ├── service/                          # 服务接口层
│   │   │   └── impl/                         # 业务实现层（含 @Transactional 事务）
│   │   ├── dao/                              # MyBatis DAO 接口
│   │   ├── domain/                           # 实体类（7 个）
│   │   ├── vo/                               # 值对象（ItemQueryVO, PageResult）
│   │   ├── exception/                        # 业务异常 + 全局异常处理
│   │   ├── interceptor/                      # 登录拦截器 + 管理员拦截器
│   │   └── utils/MD5Utils.java               # MD5 加密工具类
│   ├── src/main/resources/
│   │   ├── application.yml                   # 主配置（端口 8080, MyBatis, 日志级别）
│   │   ├── application-dev.yml               # 开发环境配置
│   │   ├── application-prod.yml              # 生产环境配置
│   │   └── mapper/                           # MyBatis XML 映射文件（7 个）
│   ├── campus_bazaar.sql                     # 完整建库建表 + 初始化数据脚本
│   └── pom.xml                               # Maven 依赖配置
│
├── campus-bazaar-web/                  # 前端 Vue 3 项目
│   ├── src/
│   │   ├── api/index.js                # API 接口封装（7 个模块）
│   │   ├── utils/request.js            # Axios 实例与请求拦截
│   │   ├── router/index.js             # 路由配置（含登录/管理员守卫）
│   │   ├── stores/user.js              # Pinia 用户状态管理
│   │   ├── components/                 # 通用组件（Navbar, ItemCard, Toast）
│   │   ├── views/                      # 页面视图（共 11 个）
│   │   ├── App.vue                     # 根组件
│   │   ├── main.js                     # 入口文件
│   │   └── style.css                   # 全局样式
│   ├── index.html                      # HTML 入口
│   ├── vite.config.js                  # Vite 配置
│   └── package.json                    # 前端依赖
│
└── README.md                           # 本文件
```

---

## 数据库设计

共 7 张数据表：

| 表名 | 说明 | 核心字段 |
|------|------|---------|
| `cb_user` | 用户表（买家/卖家/管理员） | username, password(MD5), nickname, school, credit_score, role, status |
| `cb_category` | 商品分类表 | name(唯一), icon, sort |
| `cb_item` | 商品表 | seller_id, category_id, title, price, status(0-4), view_count, fav_count |
| `cb_order` | 订单表 | order_no(唯一), item_id, buyer_id, seller_id, status(0-3), meet_place |
| `cb_comment` | 留言表（支持嵌套回复） | item_id, user_id, content(≤200字), reply_id(自关联) |
| `cb_favorite` | 收藏表 | user_id + item_id(唯一联合) |
| `cb_review` | 评价表（一单一评） | order_id(唯一), reviewer_id, reviewee_id, score(1-5), content(≤300字) |

### 数据关系

- **商品** → 用户（卖家）多对一，**商品** → 分类多对一
- **订单** → 商品一对一，**订单** → 买家/卖家多对一
- **评价** → 订单一对一
- **留言** → 商品多对一，**留言** → 留言自关联（嵌套回复）
- **收藏** → 商品多对一（联合唯一防重复收藏）

---

## RESTful API 概览

共 33 个接口，Session 维持登录态。

### 公开接口（无需登录）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/categories` | 获取全部分类 |
| GET | `/api/items` | 商品列表（分类/关键词/排序/分页） |
| GET | `/api/items/{id}` | 商品详情 |
| GET | `/api/items/seller/{sellerId}` | 卖家所有商品 |
| GET | `/api/items/seller/{sellerId}/onsale` | 卖家在售商品 |
| GET | `/api/comments/item/{itemId}` | 商品留言（含嵌套回复） |
| GET | `/api/reviews/item/{itemId}` | 商品评价 |
| GET | `/api/users/{id}` | 用户公开信息 |

### 需登录接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/users/register` | 注册 |
| POST | `/api/users/login` | 登录 |
| POST | `/api/users/logout` | 退出 |
| GET | `/api/users/me` | 当前用户信息 |
| PUT | `/api/users/me` | 修改个人信息 |
| GET | `/api/users/me/favorites` | 我的收藏 |
| POST | `/api/items` | 发布商品 |
| PUT | `/api/items/{id}` | 编辑商品 |
| DELETE | `/api/items/{id}` | 下架商品 |
| POST | `/api/items/{id}/favorite` | 收藏商品 |
| DELETE | `/api/items/{id}/favorite` | 取消收藏 |
| POST | `/api/orders` | 提交订单 |
| GET | `/api/orders/buy` | 我买到的订单 |
| GET | `/api/orders/sell` | 我卖出的订单 |
| GET | `/api/orders/item/{itemId}` | 商品关联订单 |
| PUT | `/api/orders/{id}/confirm` | 卖家确认订单 |
| PUT | `/api/orders/{id}/finish` | 买家完成交易 |
| PUT | `/api/orders/{id}/cancel` | 取消订单 |
| POST | `/api/comments` | 新增留言 |
| POST | `/api/comments/{id}/reply` | 回复留言 |
| GET | `/api/reviews/check/{orderId}` | 能否评价 |
| POST | `/api/reviews` | 提交评价 |

### 管理员接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/users` | 用户列表（分页） |
| PUT | `/api/admin/users/{id}/status` | 启用/禁用用户 |
| GET | `/api/admin/items` | 商品列表（含待审核） |
| PUT | `/api/admin/items/{id}/status` | 审核/下架商品 |

---

## 快速启动

### 环境要求

- JDK 1.8+
- Maven 3.6+
- MySQL 8.0+
- Node.js 16+
- npm 或 pnpm

### 1. 初始化数据库

使用 MySQL 客户端或 Navicat 执行初始化脚本：

```bash
mysql -u root -p < campus-bazaar-boot/campus_bazaar.sql
```

脚本会创建 `campus_bazaar` 数据库及全部 7 张表，并插入测试数据。

### 2. 启动后端

```bash
cd campus-bazaar-boot
# 修改 application-dev.yml 中的数据库连接信息（url、username、password）
mvn spring-boot:run
```

后端默认运行在 `http://localhost:8080`。

### 3. 启动前端

```bash
cd campus-bazaar-web
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`。

### 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `123456` | 管理员 |
| `zhangsan` | `123456` | 普通用户（卖家） |
| `lisi` | `123456` | 普通用户（买家/卖家） |
| `wangwu` | `123456` | 普通用户 |

---

## 关键业务逻辑

### 订单状态流转

```
待确认 (0) ──[卖家确认]──▶ 已确认 (1) ──[买家完成]──▶ 已完成 (2)
     │                                                    │
     └──[任一方取消]──▶ 已取消 (3)                        └── 不可取消
```

事务联动：**提交订单**时商品 `1(在售) → 2(锁定)`，**取消订单**时商品 `2(锁定) → 1(在售)`，**完成交易**时订单 `已完成` + 商品 `已售出` + 卖家信用分 `+2`，三者通过 `@Transactional` 保证原子性。

### 商品状态码

| 状态 | 含义 |
|------|------|
| 0 | 待审核（新发布默认） |
| 1 | 在售（公开可见） |
| 2 | 锁定（已有人下单，不可购买） |
| 3 | 已售出 |
| 4 | 下架 |

---

## 日志与排查

- **SQL 日志**：已配置 `com.bazaar.dao: debug`，控制台可查看每条 MyBatis 执行的 SQL 及参数
- **慢查询**：结合 MySQL `slow_query_log` 与日志中的接口响应时长定位性能瓶颈
- **日志格式**：`时间 [线程] 级别 类名 - 消息`
