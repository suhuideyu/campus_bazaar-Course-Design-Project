-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-042    所属域：05_订单一致性
-- 校验目标：订单号超长
-- 判定标准：订单号 VARCHAR(32)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, CHAR_LENGTH(order_no) L FROM cb_order WHERE CHAR_LENGTH(order_no) > 32;
