-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-015    所属域：02_用户一致性
-- 校验目标：状态值非法
-- 判定标准：status 取值 0-禁用 1-正常
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, status FROM cb_user WHERE status NOT IN (0, 1);
