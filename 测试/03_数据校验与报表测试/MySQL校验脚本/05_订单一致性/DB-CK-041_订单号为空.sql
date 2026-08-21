-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-041    所属域：05_订单一致性
-- 校验目标：订单号为空
-- 判定标准：订单号必填
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id FROM cb_order WHERE order_no IS NULL OR order_no = '';
