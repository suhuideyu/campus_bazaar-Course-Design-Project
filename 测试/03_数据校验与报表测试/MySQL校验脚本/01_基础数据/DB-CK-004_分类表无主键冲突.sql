-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-004    所属域：01_基础数据
-- 校验目标：分类表无主键冲突
-- 判定标准：id 为主键，不应重复
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, COUNT(*) c FROM cb_category GROUP BY id HAVING c > 1;
