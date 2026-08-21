-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-035    所属域：04_收藏一致性
-- 校验目标：同一用户重复收藏同一商品
-- 判定标准：(user_id,item_id) 唯一约束，不应重复收藏
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT user_id, item_id, COUNT(*) c FROM cb_favorite GROUP BY user_id, item_id HAVING c > 1;
