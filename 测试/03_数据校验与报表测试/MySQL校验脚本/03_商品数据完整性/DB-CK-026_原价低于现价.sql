-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-026    所属域：03_商品数据完整性
-- 校验目标：原价低于现价
-- 判定标准：业务上原价一般不低于现价，出现此情况需人工确认
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, title, price, original_price FROM cb_item WHERE original_price IS NOT NULL AND original_price < price;
