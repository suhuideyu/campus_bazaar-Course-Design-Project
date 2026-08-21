-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-075    所属域：08_评价一致性
-- 校验目标：评价订单外键悬空
-- 判定标准：评价 order_id 必须对应真实订单
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT r.id, r.order_id FROM cb_review r WHERE NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.id = r.order_id);
