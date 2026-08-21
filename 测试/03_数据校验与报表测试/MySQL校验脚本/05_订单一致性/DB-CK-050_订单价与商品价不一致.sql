-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-050    所属域：05_订单一致性
-- 校验目标：订单价与商品价不一致
-- 判定标准：订单成交价应与商品当前价一致（交易中商品不可改价）
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.order_no, o.price order_price, it.price item_price FROM cb_order o JOIN cb_item it ON it.id = o.item_id WHERE o.price <> it.price;
