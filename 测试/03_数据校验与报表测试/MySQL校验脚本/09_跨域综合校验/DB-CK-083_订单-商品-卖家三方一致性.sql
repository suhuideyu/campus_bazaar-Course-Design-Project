-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-083    所属域：09_跨域综合校验
-- 校验目标：订单-商品-卖家三方一致性
-- 判定标准：订单、商品、卖家三者关键字段应一致
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id order_id, o.order_no, o.buyer_id, o.seller_id, it.seller_id item_seller, o.price, it.price item_price FROM cb_order o JOIN cb_item it ON it.id = o.item_id WHERE o.seller_id <> it.seller_id OR o.price <> it.price;
