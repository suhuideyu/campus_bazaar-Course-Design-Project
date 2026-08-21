-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-065    所属域：06_交易状态一致性
-- 校验目标：确认时间早于下单时间
-- 判定标准：confirmed_at 不应早于 created_at
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no, created_at, confirmed_at FROM cb_order WHERE confirmed_at IS NOT NULL AND confirmed_at < created_at;
