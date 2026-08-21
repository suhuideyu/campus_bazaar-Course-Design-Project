-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-036    所属域：04_收藏一致性
-- 校验目标：收藏数与fav_count不一致
-- 判定标准：商品 fav_count 应与收藏表实际数量一致
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT it.id, it.fav_count, t.actual FROM cb_item it LEFT JOIN (SELECT item_id, COUNT(*) actual FROM cb_favorite GROUP BY item_id) t ON t.item_id = it.id WHERE it.fav_count <> COALESCE(t.actual, 0);
