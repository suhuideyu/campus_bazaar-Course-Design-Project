-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-078    所属域：08_评价一致性
-- 校验目标：评分非法
-- 判定标准：评分范围 1-5
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, order_id, score FROM cb_review WHERE score NOT BETWEEN 1 AND 5;
