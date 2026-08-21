-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-054    所属域：05_订单一致性
-- 校验目标：订单状态值非法
-- 判定标准：状态取值 0待确认/1已确认/2已完成/3已取消
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_no, status FROM cb_order WHERE status NOT IN (0, 1, 2, 3);
