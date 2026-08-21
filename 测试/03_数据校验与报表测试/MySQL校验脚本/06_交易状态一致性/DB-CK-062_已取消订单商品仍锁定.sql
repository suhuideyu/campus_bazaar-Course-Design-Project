-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-062    所属域：06_交易状态一致性
-- 校验目标：已取消订单商品仍锁定
-- 判定标准：订单取消(status=3)后商品应解锁，不得遗留锁定
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.order_no, i.status FROM cb_order o JOIN cb_item i ON i.id = o.item_id WHERE o.status = 3 AND i.status = 2;
