-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-009    所属域：01_基础数据
-- 校验目标：密码非MD5格式
-- 判定标准：密码应为32位MD5十六进制密文，否则存在明文存储风险
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username, password FROM cb_user WHERE password NOT REGEXP '^[0-9a-f]{32}$';
