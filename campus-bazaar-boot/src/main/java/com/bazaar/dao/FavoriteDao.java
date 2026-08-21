package com.bazaar.dao;

import com.bazaar.domain.Favorite;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 收藏 DAO 接口
 * 技术点：
 * - 收藏表是用户和商品之间的关联表，user_id + item_id 表示“某用户收藏某商品”；
 * - existsByUserIdAndItemId 使用 COUNT(*) 判断是否已收藏，避免重复插入；
 * - @Param 用来给多个参数命名，XML 中按照名称引用。
 */
public interface FavoriteDao {

    /** 查询用户的收藏列表（带商品信息） */
    List<Favorite> findByUserId(Long userId);

    /** 判断是否已收藏，存在返回 1，否则返回 0 */
    int existsByUserIdAndItemId(@Param("userId") Long userId, @Param("itemId") Long itemId);

    /** 新增收藏记录 */
    int insert(Favorite favorite);

    /** 删除收藏记录，返回受影响行数 */
    int deleteByUserIdAndItemId(@Param("userId") Long userId, @Param("itemId") Long itemId);
}
