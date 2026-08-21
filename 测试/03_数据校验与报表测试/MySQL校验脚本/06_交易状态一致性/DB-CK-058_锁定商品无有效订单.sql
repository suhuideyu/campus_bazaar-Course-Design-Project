-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-058    所属域：06_交易状态一致性
-- 校验目标：锁定商品无有效订单
-- 判定标准：商品锁定(status=2)必须存在待确认或已确认订单
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT i.id, i.status FROM cb_item i WHERE i.status = 2 AND NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.item_id = i.id AND o.status IN (0,1));
