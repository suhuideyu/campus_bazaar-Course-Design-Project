-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-051    所属域：05_订单一致性
-- 校验目标：订单卖家与商品卖家不一致
-- 判定标准：订单 seller_id 应与商品 seller_id 一致
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.order_no, o.seller_id, it.seller_id item_seller FROM cb_order o JOIN cb_item it ON it.id = o.item_id WHERE o.seller_id <> it.seller_id;
