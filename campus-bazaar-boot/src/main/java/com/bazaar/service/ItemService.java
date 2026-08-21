package com.bazaar.service;

import com.bazaar.domain.Item;
import com.bazaar.vo.ItemQueryVO;
import com.bazaar.vo.PageResult;

import java.util.List;

/**
 * 商品业务接口
 * 技术点：
 * - Service 层负责组织业务流程，如校验权限、修改状态、调用多个 DAO；
 * - Controller 调用这里的方法，不直接拼 SQL。
 */
public interface ItemService {

    /**
     * 分页查询在售商品（支持分类/关键词/排序）
     */
    PageResult<Item> getItemList(ItemQueryVO query);

    /** 获取商品详情（同时 view_count+1） */
    Item getItemDetail(Long id);

    /** 获取某卖家发布的商品 */
    List<Item> getItemsBySeller(Long sellerId);

    /** 获取某卖家发布的在售商品（仅status=1） */
    List<Item> getItemsBySellerOnSale(Long sellerId);

    /** 发布商品 */
    void publishItem(Item item);

    /** 修改商品（仅限卖家本人） */
    void updateItem(Item item, Long operatorId);

    /** 下架商品（仅限卖家本人） */
    void takeDownItem(Long itemId, Long operatorId);

    /** 收藏 */
    void addFavorite(Long userId, Long itemId);

    /** 取消收藏 */
    void removeFavorite(Long userId, Long itemId);
}