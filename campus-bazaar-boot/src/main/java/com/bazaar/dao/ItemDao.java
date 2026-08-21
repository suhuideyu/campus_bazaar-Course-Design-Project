package com.bazaar.dao;
import com.bazaar.domain.Item;
import com.bazaar.vo.ItemQueryVO;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface ItemDao {
    
    /** 根据ID查询商品（连带查询卖家昵称和分类名） */
    Item findById(Long id);
    
    /** 动态条件查询商品列表（支持分类筛选、关键词、状态过滤） */
    List<Item> findByCondition(ItemQueryVO query);
    
    /** 根据卖家ID查询其发布的商品 */
    List<Item> findBySellerId(Long sellerId);

    /** 根据卖家ID查询其在售商品（仅status=1） */
    List<Item> findBySellerIdOnSale(Long sellerId);
    
    /** 插入新商品，返回自增主键 */
    int insert(Item item);
    
    /** 更新商品信息 */
    int update(Item item);
    
    /** 只更新商品状态（轻量操作） */
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);
    
    /** 浏览量+1 */
    int increaseViewCount(Long id);
    
    /** 收藏量+1 */
    int increaseFavCount(Long id);
    
    /** 收藏量-1 */
    int decreaseFavCount(Long id);

    /** 用户收藏商品（插入收藏记录） */
    int addFavorite(@Param("userId") Long userId, @Param("itemId") Long itemId);

    long countByCondition(ItemQueryVO query);
}