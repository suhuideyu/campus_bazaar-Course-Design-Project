-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-055    所属域：05_订单一致性
-- 校验目标：待确认订单缺下单时间
-- 判定标准：created_at 必填
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no FROM cb_order WHERE status = 0 AND created_at IS NULL;
