-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-003    所属域：01_基础数据
-- 校验目标：分类排序字段缺失
-- 判定标准：sort 应有默认值0，不允许空
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, name FROM cb_category WHERE sort IS NULL;
