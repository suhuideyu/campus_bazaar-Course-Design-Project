-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-034    所属域：04_收藏一致性
-- 校验目标：收藏商品外键悬空
-- 判定标准：收藏 item_id 必须对应真实商品
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT f.id, f.item_id FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id = f.item_id);
