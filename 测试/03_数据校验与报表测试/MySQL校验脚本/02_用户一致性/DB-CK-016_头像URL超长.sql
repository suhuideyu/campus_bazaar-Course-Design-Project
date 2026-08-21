-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-016    所属域：02_用户一致性
-- 校验目标：头像URL超长
-- 判定标准：头像URL VARCHAR(255)
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, CHAR_LENGTH(avatar) L FROM cb_user WHERE avatar IS NOT NULL AND CHAR_LENGTH(avatar) > 255;
