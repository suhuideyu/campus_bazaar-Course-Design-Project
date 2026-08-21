-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-073    所属域：07_留言一致性
-- 校验目标：回复指向不存在留言
-- 判定标准：reply_id 必须指向存在的留言
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT c.id, c.reply_id FROM cb_comment c WHERE c.reply_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM cb_comment p WHERE p.id = c.reply_id);
