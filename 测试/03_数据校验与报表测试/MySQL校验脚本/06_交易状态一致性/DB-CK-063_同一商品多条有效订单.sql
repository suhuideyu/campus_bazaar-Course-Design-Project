-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-063    所属域：06_交易状态一致性
-- 校验目标：同一商品多条有效订单
-- 判定标准：同一商品同时只允许一条有效订单（防重复购买）
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT item_id, COUNT(*) c FROM cb_order WHERE status IN (0,1,2) GROUP BY item_id HAVING c > 1;
