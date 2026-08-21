-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-020    所属域：02_用户一致性
-- 校验目标：禁用用户仍有在售商品
-- 判定标准：被禁用用户不应存在在售商品，需业务确认处理策略
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT i.id item_id, i.seller_id, u.username FROM cb_item i JOIN cb_user u ON u.id = i.seller_id WHERE u.status = 0 AND i.status = 1;
