-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-049    所属域：05_订单一致性
-- 校验目标：订单价格为负
-- 判定标准：成交价不应为负
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no, price FROM cb_order WHERE price < 0;
