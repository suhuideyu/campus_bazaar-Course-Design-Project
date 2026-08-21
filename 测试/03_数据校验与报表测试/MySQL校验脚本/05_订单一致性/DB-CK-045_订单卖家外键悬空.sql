-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-045    所属域：05_订单一致性
-- 校验目标：订单卖家外键悬空
-- 判定标准：seller_id 必须对应真实用户
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT o.id, o.seller_id FROM cb_order o WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = o.seller_id);
