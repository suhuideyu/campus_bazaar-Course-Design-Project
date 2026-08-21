-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-022    所属域：03_商品数据完整性
-- 校验目标：商品标题超长
-- 判定标准：标题 VARCHAR(50)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, CHAR_LENGTH(title) L FROM cb_item WHERE CHAR_LENGTH(title) > 50;
