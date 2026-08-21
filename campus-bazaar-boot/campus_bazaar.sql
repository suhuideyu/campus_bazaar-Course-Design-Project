/*
  校园二手集市数据库初始化脚本
  功能：创建数据库、数据表并初始化基础数据
  适配数据库：MySQL 8.0+
  编码格式：UTF8MB4（支持emoji等特殊字符）
*/ -- 1. 创建数据库（如果不存在）
CREATE DATABASE
IF
  NOT EXISTS campus_bazaar DEFAULT CHARACTER
  SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;-- 2. 使用该数据库
USE campus_bazaar;-- 3. 关闭外键约束检查（避免建表顺序导致的外键报错）

SET FOREIGN_KEY_CHECKS = 0;
/*
  ====================== 数据表创建 ======================
*/-- ----------------------------
-- 商品分类表 (cb_category)
-- 存储二手商品的分类信息
-- ----------------------------
DROP TABLE
    IF
    EXISTS `cb_category`;
CREATE TABLE `cb_category` (
                               `id` INT NOT NULL AUTO_INCREMENT COMMENT '分类ID（自增主键）',
                               `name` VARCHAR ( 20 ) NOT NULL COMMENT '分类名称（唯一）',
                               `icon` VARCHAR ( 50 ) DEFAULT NULL COMMENT '分类图标名称（前端使用）',
                               `sort` INT DEFAULT 0 COMMENT '排序权重（数值越大越靠前）',
                               PRIMARY KEY ( `id` ) USING BTREE,
                               UNIQUE INDEX `name` ( `name` ASC ) USING BTREE -- 分类名唯一约束

) ENGINE = InnoDB AUTO_INCREMENT = 6 DEFAULT CHARSET = utf8mb4 COMMENT = '商品分类表';
-- ----------------------------
-- 用户表 (cb_user)
-- 存储平台用户信息（买家/卖家/管理员）
-- ----------------------------
DROP TABLE
    IF
    EXISTS `cb_user`;
CREATE TABLE `cb_user` (
                           `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '用户ID（自增主键）',
                           `username` VARCHAR ( 30 ) NOT NULL COMMENT '登录用户名（唯一）',
                           `password` VARCHAR ( 64 ) NOT NULL COMMENT '密码（MD5加密存储）',
                           `nickname` VARCHAR ( 30 ) NOT NULL COMMENT '用户昵称',
                           `avatar` VARCHAR ( 255 ) DEFAULT NULL COMMENT '用户头像URL',
                           `phone` VARCHAR ( 11 ) DEFAULT NULL COMMENT '手机号（11位）',
                           `school` VARCHAR ( 50 ) DEFAULT NULL COMMENT '所在学校',
                           `credit_score` INT DEFAULT 100 COMMENT '信用分（0-200，初始100）',
                           `role` TINYINT DEFAULT 0 COMMENT '角色：0-普通用户，1-管理员',
                           `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
                           `created_at` DATETIME NOT NULL COMMENT '注册时间',
                           `updated_at` DATETIME DEFAULT NULL COMMENT '最后更新时间',
                           PRIMARY KEY ( `id` ) USING BTREE,
                           UNIQUE INDEX `username` ( `username` ASC ) USING BTREE -- 用户名唯一约束

) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4 COMMENT = '用户表';-- ----------------------------
-- 商品表 (cb_item)
-- 存储二手商品的核心信息
-- ----------------------------
DROP TABLE
    IF
    EXISTS `cb_item`;
CREATE TABLE `cb_item` (
                           `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '商品ID（自增主键）',
                           `seller_id` BIGINT NOT NULL COMMENT '卖家用户ID（关联cb_user.id）',
                           `category_id` INT NOT NULL COMMENT '分类ID（关联cb_category.id）',
                           `title` VARCHAR ( 50 ) NOT NULL COMMENT '商品标题',
                           `description` TEXT DEFAULT NULL COMMENT '商品详细描述',
                           `images` VARCHAR ( 500 ) DEFAULT NULL COMMENT '商品图片URL（逗号分隔多个URL）',
                           `price` DECIMAL ( 10, 2 ) NOT NULL COMMENT '售价（保留2位小数）',
                           `original_price` DECIMAL ( 10, 2 ) DEFAULT NULL COMMENT '原价（保留2位小数）',
                           `condition_level` TINYINT DEFAULT 3 COMMENT '商品成色：1-几乎全新，2-轻微使用，3-中度使用，4-重度使用，5-大量使用痕迹',
                           `status` TINYINT DEFAULT 0 COMMENT '商品状态：0-待审核，1-在售，2-锁定，3-已售，4-下架',
                           `view_count` INT DEFAULT 0 COMMENT '商品浏览次数',
                           `fav_count` INT DEFAULT 0 COMMENT '商品收藏次数',
                           `created_at` DATETIME NOT NULL COMMENT '发布时间',
                           `updated_at` DATETIME DEFAULT NULL COMMENT '更新时间',
                           PRIMARY KEY ( `id` ) USING BTREE,
                           INDEX `fk_item_seller` ( `seller_id` ASC ) USING BTREE,-- 卖家索引
                           INDEX `fk_item_category` ( `category_id` ASC ) USING BTREE,-- 分类索引
-- 外键约束
                           CONSTRAINT `fk_item_category` FOREIGN KEY ( `category_id` ) REFERENCES `cb_category` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT,
                           CONSTRAINT `fk_item_seller` FOREIGN KEY ( `seller_id` ) REFERENCES `cb_user` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 DEFAULT CHARSET = utf8mb4 COMMENT = '商品表';-- ----------------------------
-- 商品留言表 (cb_comment)
-- 存储商品的留言/回复信息
-- ----------------------------
DROP TABLE
    IF
    EXISTS `cb_comment`;
CREATE TABLE `cb_comment` (
                              `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '留言ID（自增主键）',
                              `item_id` BIGINT NOT NULL COMMENT '商品ID（关联cb_item.id）',
                              `user_id` BIGINT NOT NULL COMMENT '留言用户ID（关联cb_user.id）',
                              `content` VARCHAR ( 200 ) NOT NULL COMMENT '留言内容（200字以内）',
                              `reply_id` BIGINT DEFAULT NULL COMMENT '回复的父留言ID（NULL表示根留言）',
                              `created_at` DATETIME NOT NULL COMMENT '留言时间',
                              PRIMARY KEY ( `id` ) USING BTREE,
                              INDEX `fk_comment_item` ( `item_id` ASC ) USING BTREE,-- 商品索引
                              INDEX `fk_comment_user` ( `user_id` ASC ) USING BTREE,-- 用户索引
-- 外键约束
                              CONSTRAINT `fk_comment_item` FOREIGN KEY ( `item_id` ) REFERENCES `cb_item` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT,
                              CONSTRAINT `fk_comment_user` FOREIGN KEY ( `user_id` ) REFERENCES `cb_user` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4 COMMENT = '商品留言表';
-- ----------------------------
-- 收藏表 (cb_favorite)
-- 存储用户收藏商品的记录
-- ----------------------------
DROP TABLE
    IF
    EXISTS `cb_favorite`;
CREATE TABLE `cb_favorite` (
                               `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '收藏ID（自增主键）',
                               `user_id` BIGINT NOT NULL COMMENT '用户ID（关联cb_user.id）',
                               `item_id` BIGINT NOT NULL COMMENT '商品ID（关联cb_item.id）',
                               `created_at` DATETIME NOT NULL COMMENT '收藏时间',
                               PRIMARY KEY ( `id` ) USING BTREE,
                               UNIQUE INDEX `uk_user_item` ( `user_id` ASC, `item_id` ASC ) USING BTREE,-- 同一用户不能重复收藏同一商品
                               INDEX `fk_fav_item` ( `item_id` ASC ) USING BTREE,-- 商品索引
-- 外键约束
                               CONSTRAINT `fk_fav_item` FOREIGN KEY ( `item_id` ) REFERENCES `cb_item` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT,
                               CONSTRAINT `fk_fav_user` FOREIGN KEY ( `user_id` ) REFERENCES `cb_user` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 DEFAULT CHARSET = utf8mb4 COMMENT = '收藏表';-- ----------------------------
-- 订单表 (cb_order)
-- 存储商品交易订单信息
-- ----------------------------
DROP TABLE
    IF
    EXISTS `cb_order`;
CREATE TABLE `cb_order` (
                            `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '订单ID（自增主键）',
                            `order_no` VARCHAR ( 32 ) NOT NULL COMMENT '订单编号（唯一）',
                            `item_id` BIGINT NOT NULL COMMENT '商品ID（关联cb_item.id）',
                            `buyer_id` BIGINT NOT NULL COMMENT '买家ID（关联cb_user.id）',
                            `seller_id` BIGINT NOT NULL COMMENT '卖家ID（冗余字段，关联cb_user.id）',
                            `price` DECIMAL ( 10, 2 ) NOT NULL COMMENT '成交价格（保留2位小数）',
                            `message` VARCHAR ( 200 ) DEFAULT NULL COMMENT '买家留言',
                            `status` TINYINT DEFAULT 0 COMMENT '订单状态：0-待确认，1-已确认，2-已完成，3-已取消',
                            `meet_place` VARCHAR ( 100 ) DEFAULT NULL COMMENT '约定交易地点',
                            `created_at` DATETIME NOT NULL COMMENT '下单时间',
                            `confirmed_at` DATETIME DEFAULT NULL COMMENT '卖家确认时间',
                            `finished_at` DATETIME DEFAULT NULL COMMENT '交易完成时间',
                            PRIMARY KEY ( `id` ) USING BTREE,
                            UNIQUE INDEX `order_no` ( `order_no` ASC ) USING BTREE,-- 订单编号唯一
                            UNIQUE INDEX `uk_order_no` ( `order_no` ASC ) USING BTREE,
                            INDEX `fk_order_item` ( `item_id` ASC ) USING BTREE,-- 商品索引
                            INDEX `fk_order_buyer` ( `buyer_id` ASC ) USING BTREE,-- 买家索引
                            INDEX `fk_order_seller` ( `seller_id` ASC ) USING BTREE,-- 卖家索引
-- 外键约束
                            CONSTRAINT `fk_order_buyer` FOREIGN KEY ( `buyer_id` ) REFERENCES `cb_user` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT,
                            CONSTRAINT `fk_order_item` FOREIGN KEY ( `item_id` ) REFERENCES `cb_item` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT,
                            CONSTRAINT `fk_order_seller` FOREIGN KEY ( `seller_id` ) REFERENCES `cb_user` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8mb4 COMMENT = '订单表';-- ----------------------------
-- 评价表 (cb_review)
-- 存储订单完成后的评价信息（一单一评）
-- ----------------------------
DROP TABLE
    IF
    EXISTS `cb_review`;
CREATE TABLE `cb_review` (
                             `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '评价ID（自增主键）',
                             `order_id` BIGINT NOT NULL COMMENT '订单ID（关联cb_order.id，唯一）',
                             `reviewer_id` BIGINT NOT NULL COMMENT '评价者ID（买家，关联cb_user.id）',
                             `reviewee_id` BIGINT NOT NULL COMMENT '被评价者ID（卖家，关联cb_user.id）',
                             `score` TINYINT NOT NULL COMMENT '评分（1-5分）',
                             `content` VARCHAR ( 300 ) DEFAULT NULL COMMENT '评价内容（300字以内）',
                             `created_at` DATETIME NOT NULL COMMENT '评价时间',
                             PRIMARY KEY ( `id` ) USING BTREE,
                             UNIQUE INDEX `order_id` ( `order_id` ASC ) USING BTREE,-- 一单一评约束
                             UNIQUE INDEX `uk_review_order` ( `order_id` ASC ) USING BTREE,
                             INDEX `fk_review_reviewer` ( `reviewer_id` ASC ) USING BTREE,-- 评价者索引
                             INDEX `fk_review_reviewee` ( `reviewee_id` ASC ) USING BTREE,-- 被评价者索引
-- 外键约束
                             CONSTRAINT `fk_review_order` FOREIGN KEY ( `order_id` ) REFERENCES `cb_order` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT,
                             CONSTRAINT `fk_review_reviewee` FOREIGN KEY ( `reviewee_id` ) REFERENCES `cb_user` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT,
                             CONSTRAINT `fk_review_reviewer` FOREIGN KEY ( `reviewer_id` ) REFERENCES `cb_user` ( `id` ) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 DEFAULT CHARSET = utf8mb4 COMMENT = '评价表';
/*
  ====================== 初始化基础数据 ======================
*/
-- ----------------------------
-- 商品分类表初始化数据
-- ----------------------------
INSERT INTO `cb_category` ( `id`, `name`, `icon`, `sort` )
VALUES
    ( 1, '数码电子', 'icon-phone', 1 ),
    ( 2, '书籍教材', 'icon-book', 2 ),
    ( 3, '服饰鞋包', 'icon-clothes', 3 ),
    ( 4, '运动户外', 'icon-sport', 4 ),
    ( 5, '生活家居', 'icon-home', 5 );
-- ----------------------------
-- 用户表初始化数据（密码均为123456，MD5加密后：e10adc3949ba59abbe56e057f20f883e）
-- ----------------------------
INSERT INTO `cb_user` ( `id`, `username`, `password`, `nickname`, `avatar`, `phone`, `school`, `credit_score`, `role`, `status`, `created_at`, `updated_at` )
VALUES
    ( 1, 'admin', 'e10adc3949ba59abbe56e057f20f883e', '管理员', NULL, '13800138000', 'XX大学', 200, 1, 1, '2026-04-15 16:09:58', NULL ),
    ( 2, 'zhangsan', 'e10adc3949ba59abbe56e057f20f883e', '张三同学', NULL, '13800138001', 'XX大学', 195, 0, 1, '2026-04-15 16:09:58', NULL ),
    ( 3, 'lisi', 'e10adc3949ba59abbe56e057f20f883e', '李四学长', NULL, '13800138002', 'XX大学', 190, 0, 1, '2026-04-15 16:09:58', NULL ),
    ( 4, 'wangwu', 'e10adc3949ba59abbe56e057f20f883e', '王五学妹', NULL, '13800138003', 'XX大学', 180, 0, 1, '2026-04-15 16:09:58', NULL );-- ----------------------------
-- 商品表初始化数据
-- ----------------------------
INSERT INTO `cb_item` (
    `id`,
    `seller_id`,
    `category_id`,
    `title`,
    `description`,
    `images`,
    `price`,
    `original_price`,
    `condition_level`,
    `status`,
    `view_count`,
    `fav_count`,
    `created_at`,
    `updated_at`
)
VALUES
    (
        1,
        2,
        1,
        '二手AirPods Pro',
        '去年购入，功能完好，带充电盒，轻微使用痕迹',
        NULL,
        650.00,
        1599.00,
        2,
        1,
        120,
        8,
        '2026-04-15 16:10:10',
        NULL
    ),
    (
        2,
        3,
        2,
        '计算机组成原理教材',
        '正版教材，几乎全新，无笔记，送配套习题',
        NULL,
        20.00,
        49.80,
        1,
        1,
        85,
        5,
        '2026-04-15 16:10:10',
        NULL
    ),
    (
        3,
        2,
        3,
        '闲置Levi\'s牛仔裤',
    '穿过两次，版型不合适，几乎全新，尺码29',
    NULL,
    120.00,
    399.00,
    1,
    1,
    60,
    3,
    '2026-04-15 16:10:10',
  NULL
  ),
  (
    4,
    4,
    4,
    '全新羽毛球拍',
    '京东购入，未拆封，型号威克多9500',
    NULL,
    200.00,
    269.00,
    1,
    1,
    95,
    10,
    '2026-04-15 16:10:10',
  NULL
  ),
  (
    5,
    3,
    5,
    '宿舍床上小桌子',
    '可折叠，带卡槽，放床上追剧写作业很方便',
    NULL,
    35.00,
    69.00,
    2,
    1,
    151,
    15,
    '2026-04-15 16:10:10',
  NULL
  );
-- ----------------------------
-- 商品留言表初始化数据
-- ----------------------------
INSERT INTO `cb_comment` ( `id`, `item_id`, `user_id`, `content`, `reply_id`, `created_at` )
VALUES
  ( 1, 1, 4, '耳机降噪效果怎么样？', NULL, '2026-04-15 16:10:10' ),
  ( 2, 1, 2, '降噪没问题，日常通勤够用', 1, '2026-04-15 16:10:10' ),
  ( 3, 5, 2, '桌子承重怎么样？放电脑稳吗？', NULL, '2026-04-15 16:10:10' );-- ----------------------------
-- 收藏表初始化数据
-- ----------------------------
INSERT INTO `cb_favorite` ( `id`, `user_id`, `item_id`, `created_at` )
VALUES
  ( 1, 3, 3, '2026-04-15 16:10:10' ),
  ( 2, 4, 2, '2026-04-15 16:10:10' ),
  ( 3, 2, 4, '2026-04-15 16:10:10' ),
  ( 4, 3, 5, '2026-04-15 16:10:10' );
-- ----------------------------
-- 订单表初始化数据
-- ----------------------------
INSERT INTO `cb_order` ( `id`, `order_no`, `item_id`, `buyer_id`, `seller_id`, `price`, `message`, `status`, `meet_place`, `created_at`, `confirmed_at`, `finished_at` )
VALUES
  ( 1, 'ORD202604150001', 1, 3, 2, 650.00, '可以约在食堂门口交易吗？', 1, '第一食堂门口', '2026-04-15 16:10:10', '2026-04-15 16:10:10', '2026-04-15 16:10:10' ),
  ( 2, 'ORD202604150002', 5, 2, 3, 35.00, '我今天下午有空', 1, '图书馆楼下', '2026-04-15 16:10:10', '2026-04-15 16:10:10', NULL ),
  ( 3, 'TEST1777275514639', 1, 2, 3, 88.80, NULL, 0, NULL, '2026-04-27 15:38:35', NULL, NULL );
-- ----------------------------
-- 评价表初始化数据
-- ----------------------------
INSERT INTO `cb_review` ( `id`, `order_id`, `reviewer_id`, `reviewee_id`, `score`, `content`, `created_at` )
VALUES
  ( 1, 1, 3, 2, 5, '卖家很爽快，商品和描述一致，推荐！', '2026-04-15 16:10:10' );-- 4. 恢复外键约束检查

SET FOREIGN_KEY_CHECKS = 1;-- 执行完成提示
SELECT
  '数据库初始化完成！' AS `status`;