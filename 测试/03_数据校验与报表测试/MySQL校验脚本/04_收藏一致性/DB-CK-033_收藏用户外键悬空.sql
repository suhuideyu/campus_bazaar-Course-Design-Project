-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-033    所属域：04_收藏一致性
-- 校验目标：收藏用户外键悬空
-- 判定标准：收藏 user_id 必须对应真实用户
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT f.id, f.user_id FROM cb_favorite f WHERE NOT EXISTS (SELECT 1 FROM cb_user u WHERE u.id = f.user_id);
