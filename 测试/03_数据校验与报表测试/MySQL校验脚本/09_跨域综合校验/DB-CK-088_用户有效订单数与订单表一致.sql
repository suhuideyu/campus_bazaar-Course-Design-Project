-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-088    所属域：09_跨域综合校验
-- 校验目标：用户有效订单数与订单表一致
-- 判定标准：普通用户应至少能通过订单表检索到其交易（关注无交易用户）
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT u.id user_id, u.username FROM cb_user u LEFT JOIN cb_order o ON (o.buyer_id = u.id OR o.seller_id = u.id) WHERE o.id IS NULL AND u.role = 0;
