-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-066    所属域：06_交易状态一致性
-- 校验目标：完成时间早于确认时间
-- 判定标准：finished_at 不应早于 confirmed_at
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no, confirmed_at, finished_at FROM cb_order WHERE finished_at IS NOT NULL AND confirmed_at IS NOT NULL AND finished_at < confirmed_at;
