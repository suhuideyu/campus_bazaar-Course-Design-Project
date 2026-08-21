-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-067    所属域：06_交易状态一致性
-- 校验目标：订单完成时间缺失
-- 判定标准：已完成订单应记录 finished_at
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no FROM cb_order WHERE status = 2 AND finished_at IS NULL;
