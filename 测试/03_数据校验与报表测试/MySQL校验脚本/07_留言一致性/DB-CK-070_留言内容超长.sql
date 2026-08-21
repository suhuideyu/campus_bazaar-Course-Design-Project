-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-070    所属域：07_留言一致性
-- 校验目标：留言内容超长
-- 判定标准：content VARCHAR(200)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, CHAR_LENGTH(content) L FROM cb_comment WHERE CHAR_LENGTH(content) > 200;
