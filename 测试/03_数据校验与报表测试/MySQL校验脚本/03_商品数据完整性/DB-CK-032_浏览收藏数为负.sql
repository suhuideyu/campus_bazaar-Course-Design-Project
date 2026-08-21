-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-032    所属域：03_商品数据完整性
-- 校验目标：浏览收藏数为负
-- 判定标准：view_count/fav_count 不应为负
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, view_count, fav_count FROM cb_item WHERE view_count < 0 OR fav_count < 0;
