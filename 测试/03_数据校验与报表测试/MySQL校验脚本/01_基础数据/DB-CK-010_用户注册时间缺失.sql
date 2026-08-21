-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-010    所属域：01_基础数据
-- 校验目标：用户注册时间缺失
-- 判定标准：created_at 必填
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, username FROM cb_user WHERE created_at IS NULL;
