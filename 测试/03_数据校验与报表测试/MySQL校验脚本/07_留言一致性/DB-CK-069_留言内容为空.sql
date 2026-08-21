-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-069    所属域：07_留言一致性
-- 校验目标：留言内容为空
-- 判定标准：留言内容必填
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT id, item_id, user_id FROM cb_comment WHERE content IS NULL OR content = '';
