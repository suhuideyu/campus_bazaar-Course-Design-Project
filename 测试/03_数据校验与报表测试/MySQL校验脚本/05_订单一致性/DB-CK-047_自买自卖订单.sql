-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-047    所属域：05_订单一致性
-- 校验目标：自买自卖订单
-- 判定标准：买卖双方不应为同一人
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no, buyer_id, seller_id FROM cb_order WHERE buyer_id = seller_id;
