-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-025    所属域：03_商品数据完整性
-- 校验目标：商品原价越界
-- 判定标准：原价应为正数且不超过 DECIMAL(10,2) 上限
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, title, original_price FROM cb_item WHERE original_price IS NOT NULL AND (original_price <= 0 OR original_price > 99999999.99);
