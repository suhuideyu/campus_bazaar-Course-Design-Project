-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-006    所属域：01_基础数据
-- 校验目标：用户名超长
-- 判定标准：用户名 VARCHAR(30)，不得超过30字符
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, CHAR_LENGTH(username) L FROM cb_user WHERE CHAR_LENGTH(username) > 30;
