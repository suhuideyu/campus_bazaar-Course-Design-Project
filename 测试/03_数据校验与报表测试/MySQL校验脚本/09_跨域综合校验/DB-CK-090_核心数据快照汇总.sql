-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-090    所属域：09_跨域综合校验
-- 校验目标：核心数据快照汇总
-- 判定标准：数据快照：返回1行汇总计数，用于与前端/报表核对
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT (SELECT COUNT(*) FROM cb_user) users, (SELECT COUNT(*) FROM cb_category) categories, (SELECT COUNT(*) FROM cb_item) items, (SELECT COUNT(*) FROM cb_order) orders, (SELECT COUNT(*) FROM cb_favorite) favorites, (SELECT COUNT(*) FROM cb_comment) comments, (SELECT COUNT(*) FROM cb_review) reviews;
