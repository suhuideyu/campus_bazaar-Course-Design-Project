-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-039    所属域：04_收藏一致性
-- 校验目标：收藏主键冲突
-- 判定标准：id 主键不应重复
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, COUNT(*) c FROM cb_favorite GROUP BY id HAVING c > 1;
