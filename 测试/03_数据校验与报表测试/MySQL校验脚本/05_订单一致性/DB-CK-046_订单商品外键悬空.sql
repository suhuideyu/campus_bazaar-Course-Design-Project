-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-046    所属域：05_订单一致性
-- 校验目标：订单商品外键悬空
-- 判定标准：item_id 必须对应真实商品
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.item_id FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id = o.item_id);
