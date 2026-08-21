-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-029    所属域：03_商品数据完整性
-- 校验目标：商品成色值非法
-- 判定标准：成色取值 1-5
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, condition_level FROM cb_item WHERE condition_level NOT BETWEEN 1 AND 5;
