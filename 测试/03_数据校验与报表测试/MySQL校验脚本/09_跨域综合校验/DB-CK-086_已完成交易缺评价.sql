-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-086    所属域：09_跨域综合校验
-- 校验目标：已完成交易缺评价
-- 判定标准：按一单一评规则，已完成交易应存在评价
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.order_no FROM cb_order o WHERE o.status = 2 AND NOT EXISTS (SELECT 1 FROM cb_review rv WHERE rv.order_id = o.id);
