-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-043    所属域：05_订单一致性
-- 校验目标：订单号重复
-- 判定标准：订单号唯一，不应重复
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT order_no, COUNT(*) c FROM cb_order GROUP BY order_no HAVING c > 1;
