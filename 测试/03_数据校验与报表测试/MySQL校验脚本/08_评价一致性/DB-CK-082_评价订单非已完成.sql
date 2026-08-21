-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-082    所属域：08_评价一致性
-- 校验目标：评价订单非已完成
-- 判定标准：评价应仅针对已完成交易(status=2)的订单
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT r.id, r.order_id, o.status FROM cb_review r JOIN cb_order o ON o.id = r.order_id WHERE o.status <> 2;
