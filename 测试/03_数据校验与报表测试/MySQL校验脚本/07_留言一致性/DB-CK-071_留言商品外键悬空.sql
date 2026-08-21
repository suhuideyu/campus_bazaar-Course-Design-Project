-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-071    所属域：07_留言一致性
-- 校验目标：留言商品外键悬空
-- 判定标准：留言 item_id 必须对应真实商品
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT c.id, c.item_id FROM cb_comment c WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id = c.item_id);
