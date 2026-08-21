-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-031    所属域：03_商品数据完整性
-- 校验目标：商品图片超长
-- 判定标准：images VARCHAR(500)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, CHAR_LENGTH(images) L FROM cb_item WHERE images IS NOT NULL AND CHAR_LENGTH(images) > 500;
