-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-002    所属域：01_基础数据
-- 校验目标：分类名超长
-- 判定标准：分类名 VARCHAR(20)，长度不得超过20
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, name, CHAR_LENGTH(name) L FROM cb_category WHERE CHAR_LENGTH(name) > 20;
