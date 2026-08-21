-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-085    所属域：09_跨域综合校验
-- 校验目标：商品状态与订单状态全量对照
-- 判定标准：全量核对商品状态与订单状态的联动关系（人工复核清单）
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT i.id item_id, i.status item_status, o.id order_id, o.status order_status FROM cb_item i LEFT JOIN cb_order o ON o.item_id = i.id AND o.status IN (0,1,2) ORDER BY i.id;
