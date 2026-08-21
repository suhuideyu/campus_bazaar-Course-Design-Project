-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-089    所属域：09_跨域综合校验
-- 校验目标：六表外键完整性总检
-- 判定标准：全表外键完整性总检，各域悬空记录数应为0
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT 'cb_item->seller' t, COUNT(*) bad FROM cb_item i WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=i.seller_id) UNION ALL SELECT 'cb_order->buyer', COUNT(*) FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=o.buyer_id) UNION ALL SELECT 'cb_order->item', COUNT(*) FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id=o.item_id) UNION ALL SELECT 'cb_comment->item', COUNT(*) FROM cb_comment c WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id=c.item_id) UNION ALL SELECT 'cb_comment->user', COUNT(*) FROM cb_comment c WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=c.user_id) UNION ALL SELECT 'cb_favorite->user', COUNT(*) FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id=f.user_id) UNION ALL SELECT 'cb_favorite->item', COUNT(*) FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_item it WHERE it.id=f.item_id) UNION ALL SELECT 'cb_review->order', COUNT(*) FROM cb_review r WHERE NOT EXISTS (SELECT 1 FROM cb_order o WHERE o.id=r.order_id);
