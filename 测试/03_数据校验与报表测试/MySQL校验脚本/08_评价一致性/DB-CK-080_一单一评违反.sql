-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-080    所属域：08_评价一致性
-- 校验目标：一单一评违反
-- 判定标准：同一订单至多一条评价（order_id 唯一约束）
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT order_id, COUNT(*) c FROM cb_review GROUP BY order_id HAVING c > 1;
