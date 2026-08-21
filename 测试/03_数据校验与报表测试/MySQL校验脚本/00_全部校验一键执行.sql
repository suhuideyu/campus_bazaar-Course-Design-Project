-- 全量执行入口：一键运行全部 90 条校验脚本
USE campus_bazaar;

-- ---------- DB-CK-001 分类名重复：cb_category.name 唯一约束，不应出现重复分类名 ----------
SELECT id, name, COUNT(*) c FROM cb_category GROUP BY name HAVING c > 1;

-- ---------- DB-CK-002 分类名超长：分类名 VARCHAR(20)，长度不得超过20 ----------
SELECT id, name, CHAR_LENGTH(name) L FROM cb_category WHERE CHAR_LENGTH(name) > 20;

-- ---------- DB-CK-003 分类排序字段缺失：sort 应有默认值0，不允许空 ----------
SELECT id, name FROM cb_category WHERE sort IS NULL;

-- ---------- DB-CK-004 分类表无主键冲突：id 为主键，不应重复 ----------
SELECT id, COUNT(*) c FROM cb_category GROUP BY id HAVING c > 1;

-- ---------- DB-CK-005 用户名重复：cb_user.username 唯一约束，不应重复 ----------
SELECT id, username, COUNT(*) c FROM cb_user GROUP BY username HAVING c > 1;

-- ---------- DB-CK-006 用户名超长：用户名 VARCHAR(30)，不得超过30字符 ----------
SELECT id, username, CHAR_LENGTH(username) L FROM cb_user WHERE CHAR_LENGTH(username) > 30;

-- ---------- DB-CK-007 昵称为空：昵称必填，不允许空 ----------
SELECT id, username FROM cb_user WHERE nickname IS NULL OR nickname = '';

-- ---------- DB-CK-008 密码为空：密码必填，不允许空 ----------
SELECT id, username FROM cb_user WHERE password IS NULL OR password = '';

-- ---------- DB-CK-009 密码非MD5格式：密码应为32位MD5十六进制密文，否则存在明文存储风险 ----------
SELECT id, username, password FROM cb_user WHERE password NOT REGEXP '^[0-9a-f]{32}$';

-- ---------- DB-CK-010 用户注册时间缺失：created_at 必填 ----------
SELECT id, username FROM cb_user WHERE created_at IS NULL;

-- ---------- DB-CK-011 手机号格式非法：手机号应为11位数字 ----------
SELECT id, username, phone FROM cb_user WHERE phone IS NOT NULL AND phone NOT REGEXP '^[0-9]{11}$';

-- ---------- DB-CK-012 学校字段超长：学校字段 VARCHAR(50) ----------
SELECT id, username, CHAR_LENGTH(school) L FROM cb_user WHERE school IS NOT NULL AND CHAR_LENGTH(school) > 50;

-- ---------- DB-CK-013 信用分越界：信用分范围 0-200 ----------
SELECT id, username, credit_score FROM cb_user WHERE credit_score < 0 OR credit_score > 200;

-- ---------- DB-CK-014 角色值非法：role 取值 0-普通用户 1-管理员 ----------
SELECT id, username, role FROM cb_user WHERE role NOT IN (0, 1);

-- ---------- DB-CK-015 状态值非法：status 取值 0-禁用 1-正常 ----------
SELECT id, username, status FROM cb_user WHERE status NOT IN (0, 1);

-- ---------- DB-CK-016 头像URL超长：头像URL VARCHAR(255) ----------
SELECT id, username, CHAR_LENGTH(avatar) L FROM cb_user WHERE avatar IS NOT NULL AND CHAR_LENGTH(avatar) > 255;

-- ---------- DB-CK-017 商品卖家外键悬空：商品 seller_id 必须对应真实用户 ----------
SELECT i.id item_id, i.seller_id FROM cb_item i WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = i.seller_id);

-- ---------- DB-CK-018 订单买家外键悬空：订单 buyer_id 必须对应真实用户 ----------
SELECT o.id order_id, o.buyer_id FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = o.buyer_id);

-- ---------- DB-CK-019 订单卖家外键悬空：订单 seller_id 必须对应真实用户 ----------
SELECT o.id order_id, o.seller_id FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = o.seller_id);

-- ---------- DB-CK-020 禁用用户仍有在售商品：被禁用用户不应存在在售商品，需业务确认处理策略 ----------
SELECT i.id item_id, i.seller_id, u.username FROM cb_item i JOIN cb_user u ON u.id = i.seller_id WHERE u.status = 0 AND i.status = 1;

-- ---------- DB-CK-021 商品标题为空：标题必填 ----------
SELECT id, seller_id FROM cb_item WHERE title IS NULL OR title = '';

-- ---------- DB-CK-022 商品标题超长：标题 VARCHAR(50) ----------
SELECT id, CHAR_LENGTH(title) L FROM cb_item WHERE CHAR_LENGTH(title) > 50;

-- ---------- DB-CK-023 商品价格为空：价格必填 ----------
SELECT id, title FROM cb_item WHERE price IS NULL;

-- ---------- DB-CK-024 商品价格非正：价格必须大于0 ----------
SELECT id, title, price FROM cb_item WHERE price <= 0;

-- ---------- DB-CK-025 商品原价越界：原价应为正数且不超过 DECIMAL(10,2) 上限 ----------
SELECT id, title, original_price FROM cb_item WHERE original_price IS NOT NULL AND (original_price <= 0 OR original_price > 99999999.99);

-- ---------- DB-CK-026 原价低于现价：业务上原价一般不低于现价，出现此情况需人工确认 ----------
SELECT id, title, price, original_price FROM cb_item WHERE original_price IS NOT NULL AND original_price < price;

-- ---------- DB-CK-027 商品分类外键悬空：category_id 必须对应真实分类 ----------
SELECT i.id, i.category_id FROM cb_item i WHERE NOT EXISTS (SELECT 1 FROM cb_category c WHERE c.id = i.category_id);

-- ---------- DB-CK-028 商品卖家外键悬空：seller_id 必须对应真实用户 ----------
SELECT i.id, i.seller_id FROM cb_item i WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = i.seller_id);

-- ---------- DB-CK-029 商品成色值非法：成色取值 1-5 ----------
SELECT id, condition_level FROM cb_item WHERE condition_level NOT BETWEEN 1 AND 5;

-- ---------- DB-CK-030 商品状态值非法：状态取值 0待审核/1在售/2锁定/3已售/4下架 ----------
SELECT id, status FROM cb_item WHERE status NOT IN (0, 1, 2, 3, 4);

-- ---------- DB-CK-031 商品图片超长：images VARCHAR(500) ----------
SELECT id, CHAR_LENGTH(images) L FROM cb_item WHERE images IS NOT NULL AND CHAR_LENGTH(images) > 500;

-- ---------- DB-CK-032 浏览收藏数为负：view_count/fav_count 不应为负 ----------
SELECT id, view_count, fav_count FROM cb_item WHERE view_count < 0 OR fav_count < 0;

-- ---------- DB-CK-033 收藏用户外键悬空：收藏 user_id 必须对应真实用户 ----------
SELECT f.id, f.user_id FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = f.user_id);

-- ---------- DB-CK-034 收藏商品外键悬空：收藏 item_id 必须对应真实商品 ----------
SELECT f.id, f.item_id FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id = f.item_id);

-- ---------- DB-CK-035 同一用户重复收藏同一商品：(user_id,item_id) 唯一约束，不应重复收藏 ----------
SELECT user_id, item_id, COUNT(*) c FROM cb_favorite GROUP BY user_id, item_id HAVING c > 1;

-- ---------- DB-CK-036 收藏数与fav_count不一致：商品 fav_count 应与收藏表实际数量一致 ----------
SELECT it.id, it.fav_count, t.actual FROM cb_item it LEFT JOIN (SELECT item_id, COUNT(*) actual FROM cb_favorite GROUP BY item_id) t ON t.item_id = it.id WHERE it.fav_count <> COALESCE(t.actual, 0);

-- ---------- DB-CK-037 收藏已删除商品：收藏的商品必须存在 ----------
SELECT f.id, f.item_id FROM cb_favorite f LEFT JOIN cb_item it ON it.id = f.item_id WHERE it.id IS NULL;

-- ---------- DB-CK-038 收藏时间缺失：收藏时间必填 ----------
SELECT id, user_id, item_id FROM cb_favorite WHERE created_at IS NULL;

-- ---------- DB-CK-039 收藏主键冲突：id 主键不应重复 ----------
SELECT id, COUNT(*) c FROM cb_favorite GROUP BY id HAVING c > 1;

-- ---------- DB-CK-040 收藏不存在商品：收藏商品必须存在（外键级校验） ----------
SELECT f.id, f.item_id FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id = f.item_id);

-- ---------- DB-CK-041 订单号为空：订单号必填 ----------
SELECT id FROM cb_order WHERE order_no IS NULL OR order_no = '';

-- ---------- DB-CK-042 订单号超长：订单号 VARCHAR(32) ----------
SELECT id, CHAR_LENGTH(order_no) L FROM cb_order WHERE CHAR_LENGTH(order_no) > 32;

-- ---------- DB-CK-043 订单号重复：订单号唯一，不应重复 ----------
SELECT order_no, COUNT(*) c FROM cb_order GROUP BY order_no HAVING c > 1;

-- ---------- DB-CK-044 订单买家外键悬空：buyer_id 必须对应真实用户 ----------
SELECT o.id, o.buyer_id FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = o.buyer_id);

-- ---------- DB-CK-045 订单卖家外键悬空：seller_id 必须对应真实用户 ----------
SELECT o.id, o.seller_id FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = o.seller_id);

-- ---------- DB-CK-046 订单商品外键悬空：item_id 必须对应真实商品 ----------
SELECT o.id, o.item_id FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id = o.item_id);

-- ---------- DB-CK-047 自买自卖订单：买卖双方不应为同一人 ----------
SELECT id, order_no, buyer_id, seller_id FROM cb_order WHERE buyer_id = seller_id;

-- ---------- DB-CK-048 订单价格为空：成交价必填 ----------
SELECT id, order_no FROM cb_order WHERE price IS NULL;

-- ---------- DB-CK-049 订单价格为负：成交价不应为负 ----------
SELECT id, order_no, price FROM cb_order WHERE price < 0;

-- ---------- DB-CK-050 订单价与商品价不一致：订单成交价应与商品当前价一致（交易中商品不可改价） ----------
SELECT o.id, o.order_no, o.price order_price, it.price item_price FROM cb_order o JOIN cb_item it ON it.id = o.item_id WHERE o.price <> it.price;

-- ---------- DB-CK-051 订单卖家与商品卖家不一致：订单 seller_id 应与商品 seller_id 一致 ----------
SELECT o.id, o.order_no, o.seller_id, it.seller_id item_seller FROM cb_order o JOIN cb_item it ON it.id = o.item_id WHERE o.seller_id <> it.seller_id;

-- ---------- DB-CK-052 订单留言超长：message VARCHAR(200) ----------
SELECT id, CHAR_LENGTH(message) L FROM cb_order WHERE message IS NOT NULL AND CHAR_LENGTH(message) > 200;

-- ---------- DB-CK-053 交易地点超长：meet_place VARCHAR(100) ----------
SELECT id, CHAR_LENGTH(meet_place) L FROM cb_order WHERE meet_place IS NOT NULL AND CHAR_LENGTH(meet_place) > 100;

-- ---------- DB-CK-054 订单状态值非法：状态取值 0待确认/1已确认/2已完成/3已取消 ----------
SELECT id, order_no, status FROM cb_order WHERE status NOT IN (0, 1, 2, 3);

-- ---------- DB-CK-055 待确认订单缺下单时间：created_at 必填 ----------
SELECT id, order_no FROM cb_order WHERE status = 0 AND created_at IS NULL;

-- ---------- DB-CK-056 已确认订单缺确认时间：已确认订单应记录 confirmed_at ----------
SELECT id, order_no FROM cb_order WHERE status = 1 AND confirmed_at IS NULL;

-- ---------- DB-CK-057 已售商品无已完成订单：商品已售(status=3)必须存在对应已完成订单 ----------
SELECT i.id, i.status FROM cb_item i WHERE i.status = 3 AND NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.item_id = i.id AND o.status = 2);

-- ---------- DB-CK-058 锁定商品无有效订单：商品锁定(status=2)必须存在待确认或已确认订单 ----------
SELECT i.id, i.status FROM cb_item i WHERE i.status = 2 AND NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.item_id = i.id AND o.status IN (0,1));

-- ---------- DB-CK-059 已完成订单商品非已售：订单完成(status=2)时商品应同步为已售(status=3) ----------
SELECT o.id, o.order_no, o.status, i.status item_status FROM cb_order o JOIN cb_item i ON i.id = o.item_id WHERE o.status = 2 AND i.status <> 3;

-- ---------- DB-CK-060 待确认订单商品非锁定：订单待确认(status=0)时商品应为锁定(status=2) ----------
SELECT o.id, o.order_no, i.status FROM cb_order o JOIN cb_item i ON i.id = o.item_id WHERE o.status = 0 AND i.status <> 2;

-- ---------- DB-CK-061 已确认订单商品非锁定：订单已确认(status=1)时商品应为锁定(status=2) ----------
SELECT o.id, o.order_no, i.status FROM cb_order o JOIN cb_item i ON i.id = o.item_id WHERE o.status = 1 AND i.status <> 2;

-- ---------- DB-CK-062 已取消订单商品仍锁定：订单取消(status=3)后商品应解锁，不得遗留锁定 ----------
SELECT o.id, o.order_no, i.status FROM cb_order o JOIN cb_item i ON i.id = o.item_id WHERE o.status = 3 AND i.status = 2;

-- ---------- DB-CK-063 同一商品多条有效订单：同一商品同时只允许一条有效订单（防重复购买） ----------
SELECT item_id, COUNT(*) c FROM cb_order WHERE status IN (0,1,2) GROUP BY item_id HAVING c > 1;

-- ---------- DB-CK-064 取消订单仍为有效交易：已取消订单不应同时带有完成流转记录 ----------
SELECT id, order_no FROM cb_order WHERE status = 3 AND confirmed_at IS NOT NULL AND finished_at IS NOT NULL;

-- ---------- DB-CK-065 确认时间早于下单时间：confirmed_at 不应早于 created_at ----------
SELECT id, order_no, created_at, confirmed_at FROM cb_order WHERE confirmed_at IS NOT NULL AND confirmed_at < created_at;

-- ---------- DB-CK-066 完成时间早于确认时间：finished_at 不应早于 confirmed_at ----------
SELECT id, order_no, confirmed_at, finished_at FROM cb_order WHERE finished_at IS NOT NULL AND confirmed_at IS NOT NULL AND finished_at < confirmed_at;

-- ---------- DB-CK-067 订单完成时间缺失：已完成订单应记录 finished_at ----------
SELECT id, order_no FROM cb_order WHERE status = 2 AND finished_at IS NULL;

-- ---------- DB-CK-068 无有效订单的商品状态异常：非待审核/下架商品应存在关联订单 ----------
SELECT i.id, i.status FROM cb_item i WHERE i.status NOT IN (0,4) AND NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.item_id = i.id);

-- ---------- DB-CK-069 留言内容为空：留言内容必填 ----------
SELECT id, item_id, user_id FROM cb_comment WHERE content IS NULL OR content = '';

-- ---------- DB-CK-070 留言内容超长：content VARCHAR(200) ----------
SELECT id, CHAR_LENGTH(content) L FROM cb_comment WHERE CHAR_LENGTH(content) > 200;

-- ---------- DB-CK-071 留言商品外键悬空：留言 item_id 必须对应真实商品 ----------
SELECT c.id, c.item_id FROM cb_comment c WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id = c.item_id);

-- ---------- DB-CK-072 留言用户外键悬空：留言 user_id 必须对应真实用户 ----------
SELECT c.id, c.user_id FROM cb_comment c WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = c.user_id);

-- ---------- DB-CK-073 回复指向不存在留言：reply_id 必须指向存在的留言 ----------
SELECT c.id, c.reply_id FROM cb_comment c WHERE c.reply_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM cb_comment p WHERE p.id = c.reply_id);

-- ---------- DB-CK-074 留言时间缺失：created_at 必填 ----------
SELECT id FROM cb_comment WHERE created_at IS NULL;

-- ---------- DB-CK-075 评价订单外键悬空：评价 order_id 必须对应真实订单 ----------
SELECT r.id, r.order_id FROM cb_review r WHERE NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.id = r.order_id);

-- ---------- DB-CK-076 评价者外键悬空：评价者 reviewer_id 必须对应真实用户 ----------
SELECT r.id, r.reviewer_id FROM cb_review r WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = r.reviewer_id);

-- ---------- DB-CK-077 被评价者外键悬空：被评价者 reviewee_id 必须对应真实用户 ----------
SELECT r.id, r.reviewee_id FROM cb_review r WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = r.reviewee_id);

-- ---------- DB-CK-078 评分非法：评分范围 1-5 ----------
SELECT id, order_id, score FROM cb_review WHERE score NOT BETWEEN 1 AND 5;

-- ---------- DB-CK-079 评分为空：评分必填 ----------
SELECT id, order_id FROM cb_review WHERE score IS NULL;

-- ---------- DB-CK-080 一单一评违反：同一订单至多一条评价（order_id 唯一约束） ----------
SELECT order_id, COUNT(*) c FROM cb_review GROUP BY order_id HAVING c > 1;

-- ---------- DB-CK-081 评价内容超长：content VARCHAR(300) ----------
SELECT id, CHAR_LENGTH(content) L FROM cb_review WHERE content IS NOT NULL AND CHAR_LENGTH(content) > 300;

-- ---------- DB-CK-082 评价订单非已完成：评价应仅针对已完成交易(status=2)的订单 ----------
SELECT r.id, r.order_id, o.status FROM cb_review r JOIN cb_order o ON o.id = r.order_id WHERE o.status <> 2;

-- ---------- DB-CK-083 订单-商品-卖家三方一致性：订单、商品、卖家三者关键字段应一致 ----------
SELECT o.id order_id, o.order_no, o.buyer_id, o.seller_id, it.seller_id item_seller, o.price, it.price item_price FROM cb_order o JOIN cb_item it ON it.id = o.item_id WHERE o.seller_id <> it.seller_id OR o.price <> it.price;

-- ---------- DB-CK-084 收藏-商品-用户三方关联：收藏记录的买卖双方关联必须完整 ----------
SELECT f.id FROM cb_favorite f LEFT JOIN cb_user u ON u.id = f.user_id LEFT JOIN cb_item it ON it.id = f.item_id WHERE u.id IS NULL OR it.id IS NULL;

-- ---------- DB-CK-085 商品状态与订单状态全量对照：全量核对商品状态与订单状态的联动关系（人工复核清单） ----------
SELECT i.id item_id, i.status item_status, o.id order_id, o.status order_status FROM cb_item i LEFT JOIN cb_order o ON o.item_id = i.id AND o.status IN (0,1,2) ORDER BY i.id;

-- ---------- DB-CK-086 已完成交易缺评价：按一单一评规则，已完成交易应存在评价 ----------
SELECT o.id, o.order_no FROM cb_order o WHERE o.status = 2 AND NOT EXISTS (SELECT 1 FROM cb_review rv WHERE rv.order_id = o.id);

-- ---------- DB-CK-087 卖家信用分与评价联动核查：卖家信用分应与历史评价联动（人工确认计分规则） ----------
SELECT u.id seller_id, u.username, u.credit_score, t.avg_score, t.cnt FROM cb_user u LEFT JOIN (SELECT reviewee_id, ROUND(AVG(score),2) avg_score, COUNT(*) cnt FROM cb_review GROUP BY reviewee_id) t ON t.reviewee_id = u.id WHERE t.cnt > 0 AND (u.credit_score - 100) <> 0;

-- ---------- DB-CK-088 用户有效订单数与订单表一致：普通用户应至少能通过订单表检索到其交易（关注无交易用户） ----------
SELECT u.id user_id, u.username FROM cb_user u LEFT JOIN cb_order o ON (o.buyer_id = u.id OR o.seller_id = u.id) WHERE o.id IS NULL AND u.role = 0;

-- ---------- DB-CK-089 六表外键完整性总检：全表外键完整性总检，各域悬空记录数应为0 ----------
SELECT 'cb_item->seller' t, COUNT(*) bad FROM cb_item i WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=i.seller_id) UNION ALL SELECT 'cb_order->buyer', COUNT(*) FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=o.buyer_id) UNION ALL SELECT 'cb_order->item', COUNT(*) FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id=o.item_id) UNION ALL SELECT 'cb_comment->item', COUNT(*) FROM cb_comment c WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id=c.item_id) UNION ALL SELECT 'cb_comment->user', COUNT(*) FROM cb_comment c WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=c.user_id) UNION ALL SELECT 'cb_favorite->user', COUNT(*) FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=f.user_id) UNION ALL SELECT 'cb_favorite->item', COUNT(*) FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id=f.item_id) UNION ALL SELECT 'cb_review->order', COUNT(*) FROM cb_review r WHERE NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.id=r.order_id);

-- ---------- DB-CK-090 核心数据快照汇总：数据快照：返回1行汇总计数，用于与前端/报表核对 ----------
SELECT (SELECT COUNT(*) FROM cb_user) users, (SELECT COUNT(*) FROM cb_category) categories, (SELECT COUNT(*) FROM cb_item) items, (SELECT COUNT(*) FROM cb_order) orders, (SELECT COUNT(*) FROM cb_favorite) favorites, (SELECT COUNT(*) FROM cb_comment) comments, (SELECT COUNT(*) FROM cb_review) reviews;
