-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-064    所属域：06_交易状态一致性
-- 校验目标：取消订单仍为有效交易
-- 判定标准：已取消订单不应同时带有完成流转记录
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no FROM cb_order WHERE status = 3 AND confirmed_at IS NOT NULL AND finished_at IS NOT NULL;
