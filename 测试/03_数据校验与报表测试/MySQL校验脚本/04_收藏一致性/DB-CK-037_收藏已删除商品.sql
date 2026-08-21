-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-037    所属域：04_收藏一致性
-- 校验目标：收藏已删除商品
-- 判定标准：收藏的商品必须存在
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT f.id, f.item_id FROM cb_favorite f LEFT JOIN cb_item it ON it.id = f.item_id WHERE it.id IS NULL;
