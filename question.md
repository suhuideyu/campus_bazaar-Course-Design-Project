# 校园集市（Campus Bazaar）— 项目技术文档

## 1. 项目简介

校园集市是一个校园二手商品交易平台，采用前后端分离架构，支持用户发布闲置物品、浏览购买、留言交流、订单跟踪、评分评价等完整 C2C 交易流程。

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│  前端 (Vue 3 + Vite)                校园集市 Web            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │  Navbar  │ │  Router  │ │  Pinia   │ │ Element   │       │
│  │  导航栏   │ │  路由    │ │  状态管理 │ │  Plus UI │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                         │ Axios (withCredentials)           │
└─────────────────────────┼───────────────────────────────────┘
                          │ HTTP / JSON
┌─────────────────────────┼───────────────────────────────────┐
│  后端 (Spring Boot 2.7 + MyBatis)   校园集市 Boot           │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │ Login      │ │ Admin      │ │ 7 个       │               │
│  │ Interceptor│ │ Interceptor│ │ Controller │               │
│  └────────────┘ └────────────┘ └────────────┘               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │ 7 Service  │ │ 7 DAO      │ │ 7 XML      │               │
│  │  + Impl    │ │ Interface  │ │ Mapper     │               │
│  └────────────┘ └────────────┘ └────────────┘               │
│                         │                                   │
│                  MySQL 8.0 (Druid 连接池)                    │
└─────────────────────────────────────────────────────────────┘
```

### 功能模块

| 模块 | 功能 |
|------|------|
| **用户系统** | 注册、登录、个人中心、信用分（0-200） |
| **商品系统** | 发布、编辑、下架、分类浏览、关键词搜索、排序、分页 |
| **订单系统** | 预购→锁定→卖家确认→买家完成→已售，支持取消 |
| **管理员** | 用户管理（启用/禁用）、商品审核（状态变更） |
| **留言交流** | 商品详情页交流区，支持嵌套回复 |
| **评分评价** | 订单完成后买家可给卖家打分（1-5星）+ 文字评价 |

### 商品状态机

```
 发布 → 待审核(0) ──管理员审核──→ 在售(1)
                                     ↓ 买家预购
                                  锁定(2)
                               ↙         ↘
                        卖家同意        卖家/买家取消
                           ↓               ↓
                        已确认         在售(1) ← 解锁
                           ↓ 买家完成
                        已售(3) ← 买家可评价
                      
  任何状态可被卖家下架 → 下架(4)
  任何状态可被管理员强制修改
```

### 订单状态机

```
 买家提交 → 待确认(0) ──卖家同意──→ 已确认(1) ──买家完成──→ 已完成(2)
                ↕                                              ↓
                └──── 买家/卖家取消 ←──────────── 已取消(3)    可评价
```

### 数据库设计

6 张表，ER 关系如下：

```
cb_category ──┐
              ↓ (category_id FK)
cb_user ────→ cb_item ←─── cb_comment (reply_id 支持嵌套回复)
  │              │
  │ seller_id    │ item_id
  ↓              ↓
cb_order ←── cb_favorite
  │
  ↓ (order_id UNIQUE, 一单一评)
cb_review
```

---

## 2. 技术栈

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Spring Boot | 2.7.14 | 应用框架，自动配置嵌入式 Tomcat、Jackson、事务 |
| MyBatis | 2.3.2 | ORM 框架，SQL 写在 XML 中，接口无实现类 |
| Druid | 1.2.18 | 阿里数据库连接池，提供监控 |
| MySQL | 8.0 | 关系数据库，InnoDB 引擎 |
| Maven | — | 构建和依赖管理 |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.5.32 | 渐进式框架，Composition API (`<script setup>`) |
| Vite | 8.0 | 构建工具，HMR 热更新 |
| Pinia | 3.0 | 状态管理，替代 Vuex |
| Vue Router | 4.6 | SPA 路由，导航守卫 |
| Element Plus | 2.13 | UI 组件库（表格、表单、分页、评分……） |
| Axios | 1.15 | HTTP 客户端，拦截器统一处理 401 |

### 技术要点举例

**1. Spring Boot + MyBatis 动态 SQL — 商品多条件查询**

场景：首页需要支持「分类筛选 + 关键词搜索 + 排序 + 分页」组合查询，管理员还需要看所有状态。

MyBatis 的动态 `<sql>` + `<include>` + `<if>` + `<choose>` 完美解决：

```xml
<!-- ItemDao.xml -->
<sql id="dynamicWhere">
    <where>
        <if test="categoryId != null"> AND i.category_id = #{categoryId} </if>
        <if test="keyword != null"> AND i.title LIKE CONCAT('%', #{keyword}, '%') </if>
        <if test="status != null"> AND i.status = #{status} </if>
        <if test="status == null and adminMode == null">
            AND i.status = 1  <!-- 普通用户只看在售 -->
        </if>
    </where>
</sql>

<choose>
    <when test="orderBy == 'price_asc'"> ORDER BY i.price ASC </when>
    <when test="orderBy == 'hottest'">   ORDER BY i.view_count DESC </when>
    <otherwise>                          ORDER BY i.created_at DESC </otherwise>
</choose>
LIMIT #{pageSize} OFFSET #{offset}
```

一条查询覆盖 7 种场景，无需写多份 SQL。

**2. Vue 3 Composition API — `<script setup>` 语法**

场景：商品详情页需要管理商品、留言、评价、订单四组状态。Composition API 比 Options API 更利于组织逻辑：

```javascript
// ItemDetailView.vue
const item = ref(null)           // 商品数据
const comments = ref([])         // 留言树
const review = ref(null)         // 评价
const lockOrder = ref(null)      // 锁定订单（卖家可见买家信息）

const isMine = computed(() => userStore.user?.id === item.value?.sellerId)
const isBuyer = computed(() => lockOrder.value?.buyerId === userStore.user?.id)

onMounted(() => { loadItem().then(() => { loadComments(); loadReview(); loadLockOrder() }) })
```

响应式依赖自动追踪，`isMine`/`isBuyer` 随数据变化自动重算，模板自动更新。

**3. Pinia + localStorage 持久化 — 登录状态管理**

场景：用户刷新页面后仍需保持登录状态。

```javascript
// stores/user.js
const user = ref(JSON.parse(localStorage.getItem('cbUser') || 'null'))

function setUser(u) {
  user.value = u
  if (u) {
    localStorage.setItem('cbUser', JSON.stringify(u))
  } else {
    localStorage.removeItem('cbUser')
  }
}
```

刷新时从 localStorage 恢复，避免每次都要调后端 `/users/me`；导航守卫仍可同步判断 `isLoggedIn()`。

**4. Session + 拦截器 — 认证授权**

场景：除了公开页面，其他 API 需要登录；管理员 API 需要 role=1。

```java
// WebMvcConfig.java
registry.addInterceptor(new LoginInterceptor())
        .addPathPatterns("/api/**")
        .excludePathPatterns(  // 公开接口白名单
            "/api/users/login", "/api/categories", "/api/items", ...
        );

registry.addInterceptor(new AdminInterceptor())
        .addPathPatterns("/api/admin/**");  // 管理员专用
```

`LoginInterceptor` 从 HttpSession 取 `loginUser`，无则返回 401。`AdminInterceptor` 再校验 `role == 1`，否则返回 403。前端 Axios 响应拦截器统一拦截 401 跳转登录页。

**5. @Transactional 事务 — 订单流程原子性**

场景：下单需要同时「锁定商品」+「创建订单」，两步必须同时成功或同时回滚。

```java
// OrderServiceImpl.java
@Override
@Transactional(rollbackFor = Exception.class)
public Order submitOrder(Long itemId, Long buyerId, String message, String meetPlace) {
    Item item = itemDao.findById(itemId);
    if (item.getStatus() != 1) throw BusinessException.badRequest("商品不可购买");
    itemDao.updateStatus(itemId, 2);  // 锁定商品
    Order order = buildOrder(itemId, buyerId, ...);
    orderDao.insert(order);           // 创建订单
    return order;                     // 任一步失败，全部回滚
}
```

### 完整数据流举例：买家下单

```
ItemDetailView.vue (submitOrder)
  → orderApi.submit({ itemId, message, meetPlace })
    → Axios POST /api/orders (withCredentials: true, 携带 JSESSIONID cookie)
      → LoginInterceptor.preHandle() → session.getAttribute("loginUser") ✓
        → OrderController.submit()
          → OrderService.submitOrder(itemId, buyerId, message, meetPlace)
            [@Transactional 事务边界]
            → ItemDao.findById(itemId)
            → ItemDao.updateStatus(itemId, 2)   -- 锁定
            → OrderDao.insert(order)             -- 建单
            → 返回 Order
          → Result.success("订单提交成功", order)
        ← JSON { code: 200, message: "...", data: { id, orderNo, status: 0 } }
      ← Axios 拦截器: code===200, 返回 data
  → window.$toast?.('下单成功')
  → item.value.status = 2  (本地即时更新)
```

---

## 3. 核心功能讲解

### 3.1 注册与登录

**注册** ([UserController.java:42](campus-bazaar-boot/src/main/java/com/bazaar/controller/UserController.java))

- 前端校验：密码长度 ≥ 6，确认密码一致性
- 后端校验：用户名唯一性，密码 MD5 加密后入库
- MD5 加密：[MD5Utils.encrypt()](campus-bazaar-boot/src/main/java/com/bazaar/utils/MD5Utils.java) 用 `MessageDigest.getInstance("MD5")` 生成 32 位小写十六进制串
- 登录信息存入 `HttpSession`，JSESSIONID 通过 Cookie 传递给浏览器
- 后续请求由 [LoginInterceptor](campus-bazaar-boot/src/main/java/com/bazaar/interceptor/LoginInterceptor.java) 校验 Session

### 3.2 商品生命周期

**发布** → 默认为「待审核」状态（status=0），不会出现在首页。

**管理员审核**（[AdminView.vue](campus-bazaar-web/src/views/AdminView.vue) 商品管理标签页）：

- 管理员可查看所有状态的商品
- 在下拉菜单中将 status=0 改为 status=1 → 商品上架
- 也可将违规商品改为 status=4（下架）

**首页展示**（[HomeView.vue](campus-bazaar-web/src/views/HomeView.vue)）：

- 后端 SQL 默认过滤 `AND i.status = 1`，只展示在售商品
- 支持分类图标筛选、关键词标题搜索、4 种排序（综合/最新/价格升/价格降）、分页

**卖家视图**（[MyItemsView.vue](campus-bazaar-web/src/views/MyItemsView.vue)）：

- 卖家可看到自己发布的所有商品（不限状态）
- 在售商品可编辑、下架；锁定商品仅可编辑（交易中不能下架）

### 3.3 订单交易流程

整个流程有 3 个角色参与：买家、卖家、管理员。

| 步骤 | 操作 | 操作人 | 商品状态 | 订单状态 | 前端位置 |
|------|------|--------|----------|----------|----------|
| 1 | 发布商品 | 卖家 | 0 (待审核) | — | PublishView |
| 2 | 审核通过 | 管理员 | 1 (在售) | — | AdminView |
| 3 | 立即预购 | 买家 | 2 (锁定) | 0 (待确认) | ItemDetailView 下单弹窗 |
| 4 | 同意出售 | 卖家 | 2 (锁定) | 1 (已确认) | ItemDetailView "同意出售"按钮 |
| 5 | 确认完成 | 买家 | 3 (已售) | 2 (已完成) | MyOrdersView |
| 6 | 评价 | 买家 | 3 (已售) | 2 (已完成) | ItemDetailView 评价区 |
| 取消 | 任意方 | 买家/卖家 | 1 (在售) | 3 (已取消) | — |

**锁定状态下卖家查看商品详情时的体验**（[ItemDetailView.vue](campus-bazaar-web/src/views/ItemDetailView.vue)）：

- 卖家可见买家信息卡片（昵称、学校、交易地点、留言、下单时间）
- 卖家可点「同意出售」按钮继续交易（调用 `orderApi.confirm()`）
- 买家可见「等待卖家确认中…」状态提示

### 3.4 留言交流系统

**数据结构**：`cb_comment` 表用 `reply_id` 字段实现嵌套回复（NULL = 根留言）。

**后端** ([CommentServiceImpl.java](campus-bazaar-boot/src/main/java/com/bazaar/service/impl/CommentServiceImpl.java))：

- 查询时一次性加载所有留言，在 Java 内存中构建树形结构
- 将 `replyId != null` 的留言挂到对应父留言的 `replies` 列表

**前端** ([ItemDetailView.vue](campus-bazaar-web/src/views/ItemDetailView.vue) 交流区)：

- 仅在 status=1（在售）或 status=2（锁定）时显示交流区
- 根留言平铺，每条下面的回复缩进展示
- 登录用户可发表根留言或回复他人

### 3.5 评价系统

**规则**：一单一评（`cb_review.order_id` UNIQUE），仅买家可评，仅订单完成（status=2）后可评。

**前端**（[ItemDetailView.vue](campus-bazaar-web/src/views/ItemDetailView.vue) 评价区）：

- status=3（已售）时展示评价区
- 买家：若未评价 → 显示 `el-rate` 五星选择器 + 文本框
- 已评价 → 展示星级和文字

---

## 4. 加分题：棘手功能点及解决方案

### 棘手点 1：锁定商品出现在不该出现的地方

**问题**：商品被买家预购后变为锁定（status=2），但仍出现在公开的「查看Ta的其他商品」页面（[SellerItemsView.vue](campus-bazaar-web/src/views/SellerItemsView.vue)）。

**根因**：公共端点 `GET /api/items/seller/{sellerId}` 调用 `findBySellerId` SQL，该查询没有状态过滤，返回该卖家所有商品。最初前端用 `.filter(i => i.status === 1)` 做了客户端过滤，但数据先全量拉到前端再过滤，浪费带宽且不够安全。

**解决方案**：新增后端专用端点 `GET /api/items/seller/{sellerId}/onsale`，对应的 `findBySellerIdOnSale` SQL 在数据库层过滤 `AND i.status = 1`。前端 `SellerItemsView.vue` 改用新端点，彻底避免锁定商品泄露。

### 棘手点 2：卖家无法直接在商品详情页同意出售

**问题**：买家预购后商品变为锁定状态，但卖家在商品详情页只看到「编辑商品」「下架」按钮，没有「同意出售」按钮。卖家必须离开商品详情，去「我的订单」页面找到对应订单点「确认接单」。

**解决方案**：

1. 后端新增 `GET /api/orders/item/{itemId}` 端点，根据商品 ID 查询关联的活跃订单（status=0 待确认或 status=1 已确认），仅买卖家可查看
2. `Order` 实体新增 `buyerSchool` 字段，查询时 JOIN 获取买家学校信息
3. 前端 [ItemDetailView.vue](campus-bazaar-web/src/views/ItemDetailView.vue) 新增锁定状态处理：
   - 卖家：显示买家信息卡片（昵称、学校、交易地点、留言）+「同意出售」按钮
   - 买家：显示「等待卖家确认中…」
   - 其他人：显示「已被预订」
4. 同时修正操作按钮逻辑：仅在 status=1（在售）时显示编辑/下架，status=2（锁定）时下架按钮被隐藏（因为锁定商品交易中不可下架），追加「同意出售」按钮

### 棘手点 3：管理员审核机制缺失

**问题**：数据库设计已预留 `role` 字段（0=普通用户，1=管理员），但项目初期没有管理员功能模块。商品发布后默认 status=0（待审核），但无法审核通过。

**解决方案**（完整的管理员模块实现）：

1. **后端**：新增 `AdminInterceptor` 校验 `role === 1`，注册到 `/api/admin/**` 路由
2. **后端**：新增 `AdminController` 提供 4 个端点 — 用户列表、用户启禁、商品列表（含全部状态）、商品状态变更
3. **后端**：`ItemQueryVO` 新增 `adminMode` 字段，管理员查询时跳过默认的 `status=1` 过滤
4. **前端**：新增 `AdminView.vue` 管理面板，含「用户管理」「商品管理」两个标签页
5. **前端**：[Navbar.vue](campus-bazaar-web/src/components/Navbar.vue) 下拉菜单新增「管理员」入口，`v-if="user.role === 1"` 仅管理员可见
6. **前端**：路由守卫新增 `requiresAdmin` 元信息验证
