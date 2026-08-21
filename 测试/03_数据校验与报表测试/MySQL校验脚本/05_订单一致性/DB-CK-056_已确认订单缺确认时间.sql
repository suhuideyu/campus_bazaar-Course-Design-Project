-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-056    所属域：05_订单一致性
-- 校验目标：已确认订单缺确认时间
-- 判定标准：已确认订单应记录 confirmed_at
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no FROM cb_order WHERE status = 1 AND confirmed_at IS NULL;
