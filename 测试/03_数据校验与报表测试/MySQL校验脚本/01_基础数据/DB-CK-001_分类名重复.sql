-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-001    所属域：01_基础数据
-- 校验目标：分类名重复
-- 判定标准：cb_category.name 唯一约束，不应出现重复分类名
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, name, COUNT(*) c FROM cb_category GROUP BY name HAVING c > 1;
