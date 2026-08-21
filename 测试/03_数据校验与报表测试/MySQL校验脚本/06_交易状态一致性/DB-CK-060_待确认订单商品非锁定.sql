-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-060    所属域：06_交易状态一致性
-- 校验目标：待确认订单商品非锁定
-- 判定标准：订单待确认(status=0)时商品应为锁定(status=2)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.order_no, i.status FROM cb_order o JOIN cb_item i ON i.id = o.item_id WHERE o.status = 0 AND i.status <> 2;
