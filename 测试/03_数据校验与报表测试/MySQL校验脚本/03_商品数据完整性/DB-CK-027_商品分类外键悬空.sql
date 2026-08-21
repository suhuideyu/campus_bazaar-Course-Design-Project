-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-027    所属域：03_商品数据完整性
-- 校验目标：商品分类外键悬空
-- 判定标准：category_id 必须对应真实分类
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT i.id, i.category_id FROM cb_item i WHERE NOT EXISTS (SELECT 1 FROM cb_category c WHERE c.id = i.category_id);
