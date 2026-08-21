-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-017    所属域：02_用户一致性
-- 校验目标：商品卖家外键悬空
-- 判定标准：商品 seller_id 必须对应真实用户
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT i.id item_id, i.seller_id FROM cb_item i WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = i.seller_id);
