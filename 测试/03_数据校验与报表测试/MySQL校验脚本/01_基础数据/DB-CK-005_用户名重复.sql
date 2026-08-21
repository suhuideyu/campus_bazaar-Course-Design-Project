-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-005    所属域：01_基础数据
-- 校验目标：用户名重复
-- 判定标准：cb_user.username 唯一约束，不应重复
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, COUNT(*) c FROM cb_user GROUP BY username HAVING c > 1;
