-- ============================================================
-- Campus Bazaar 数据一致性校验脚本
-- 校验编号：DB-CK-084    所属域：09_跨域综合校验
-- 校验目标：收藏-商品-用户三方关联
-- 判定标准：收藏记录的买卖双方关联必须完整
-- 执行方式：mysql -uroot -p < 本文件，或在客户端执行（USE campus_bazaar）
-- ============================================================
USE campus_bazaar;

SELECT f.id FROM cb_favorite f LEFT JOIN cb_user u ON u.id = f.user_id LEFT JOIN cb_item it ON it.id = f.item_id WHERE u.id IS NULL OR it.id IS NULL;
