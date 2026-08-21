-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-053    所属域：05_订单一致性
-- 校验目标：交易地点超长
-- 判定标准：meet_place VARCHAR(100)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, CHAR_LENGTH(meet_place) L FROM cb_order WHERE meet_place IS NOT NULL AND CHAR_LENGTH(meet_place) > 100;
