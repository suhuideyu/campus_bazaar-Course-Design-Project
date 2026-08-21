-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-059    所属域：06_交易状态一致性
-- 校验目标：已完成订单商品非已售
-- 判定标准：订单完成(status=2)时商品应同步为已售(status=3)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.order_no, o.status, i.status item_status FROM cb_order o JOIN cb_item i ON i.id = o.item_id WHERE o.status = 2 AND i.status <> 3;
