-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-014    所属域：02_用户一致性
-- 校验目标：角色值非法
-- 判定标准：role 取值 0-普通用户 1-管理员
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, role FROM cb_user WHERE role NOT IN (0, 1);
