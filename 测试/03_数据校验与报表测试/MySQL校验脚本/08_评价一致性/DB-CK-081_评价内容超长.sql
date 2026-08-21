-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-081    所属域：08_评价一致性
-- 校验目标：评价内容超长
-- 判定标准：content VARCHAR(300)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, CHAR_LENGTH(content) L FROM cb_review WHERE content IS NOT NULL AND CHAR_LENGTH(content) > 300;
