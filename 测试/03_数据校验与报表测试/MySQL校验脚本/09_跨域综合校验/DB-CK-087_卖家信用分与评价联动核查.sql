-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-087    所属域：09_跨域综合校验
-- 校验目标：卖家信用分与评价联动核查
-- 判定标准：卖家信用分应与历史评价联动（人工确认计分规则）
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT u.id seller_id, u.username, u.credit_score, t.avg_score, t.cnt FROM cb_user u LEFT JOIN (SELECT reviewee_id, ROUND(AVG(score),2) avg_score, COUNT(*) cnt FROM cb_review GROUP BY reviewee_id) t ON t.reviewee_id = u.id WHERE t.cnt > 0 AND (u.credit_score - 100) <> 0;
