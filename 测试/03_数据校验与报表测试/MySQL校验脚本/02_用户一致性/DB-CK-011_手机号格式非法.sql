-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-011    所属域：02_用户一致性
-- 校验目标：手机号格式非法
-- 判定标准：手机号应为11位数字
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, phone FROM cb_user WHERE phone IS NOT NULL AND phone NOT REGEXP '^[0-9]{11}$';
