-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-012    所属域：02_用户一致性
-- 校验目标：学校字段超长
-- 判定标准：学校字段 VARCHAR(50)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, CHAR_LENGTH(school) L FROM cb_user WHERE school IS NOT NULL AND CHAR_LENGTH(school) > 50;
