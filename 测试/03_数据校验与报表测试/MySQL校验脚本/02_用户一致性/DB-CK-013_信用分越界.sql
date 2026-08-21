-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-013    所属域：02_用户一致性
-- 校验目标：信用分越界
-- 判定标准：信用分范围 0-200
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, credit_score FROM cb_user WHERE credit_score < 0 OR credit_score > 200;
