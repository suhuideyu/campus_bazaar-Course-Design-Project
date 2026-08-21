-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-068    所属域：06_交易状态一致性
-- 校验目标：无有效订单的商品状态异常
-- 判定标准：非待审核/下架商品应存在关联订单
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT i.id, i.status FROM cb_item i WHERE i.status NOT IN (0,4) AND NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.item_id = i.id);
