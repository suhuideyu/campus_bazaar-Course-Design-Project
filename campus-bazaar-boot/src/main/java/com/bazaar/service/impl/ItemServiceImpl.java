package com.bazaar.service.impl;

import com.bazaar.dao.FavoriteDao;
import com.bazaar.dao.ItemDao;
import com.bazaar.domain.Favorite;
import com.bazaar.domain.Item;
import com.bazaar.exception.BusinessException;
import com.bazaar.service.ItemService;
import com.bazaar.vo.ItemQueryVO;
import com.bazaar.vo.PageResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 商品业务实现类
 * 技术点：
 * - 商品业务包含列表查询、发布、修改、下架、收藏等用例；
 * - 涉及多次数据库修改的方法使用 @Transactional，任一步失败都会回滚；
 * - 业务异常统一抛 BusinessException，最后由 GlobalExceptionHandler 转成 JSON。
 */
@Service
public class ItemServiceImpl implements ItemService {

    private static final Logger log = LoggerFactory.getLogger(ItemServiceImpl.class);

    @Autowired
    private ItemDao itemDao;

    @Autowired
    private FavoriteDao favoriteDao;

    @Override
    public PageResult<Item> getItemList(ItemQueryVO query) {
        // 分页查询通常分两步：查当前页数据 + 查总记录数。
        List<Item> list  = itemDao.findByCondition(query);
        long       total = itemDao.countByCondition(query);
        return new PageResult<>(total, list);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Item getItemDetail(Long id) {
        Item item = itemDao.findById(id);
        if (item == null) {
            throw BusinessException.notFound("商品");
        }
        // 浏览量 +1：UPDATE view_count = view_count + 1 由数据库完成，避免并发覆盖。
        itemDao.increaseViewCount(id);
        item.setViewCount(item.getViewCount() == null ? 1 : item.getViewCount() + 1);
        return item;
    }

    @Override
    public List<Item> getItemsBySeller(Long sellerId) {
        return itemDao.findBySellerId(sellerId);
    }

    @Override
    public List<Item> getItemsBySellerOnSale(Long sellerId) {
        return itemDao.findBySellerIdOnSale(sellerId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void publishItem(Item item) {
        if (item.getTitle() == null || item.getTitle().trim().isEmpty()) {
            throw new IllegalArgumentException("商品标题不能为空");
        }
        if (item.getPrice() == null || item.getPrice().doubleValue() <= 0) {
            throw new IllegalArgumentException("商品价格必须大于 0");
        }
        if (item.getCategoryId() == null) {
            throw new IllegalArgumentException("请选择商品分类");
        }
        // 新发布：默认待审核。后续如果加管理员审核功能，可把状态从 0 改成 1。
        item.setStatus(0);
        itemDao.insert(item);
        log.info("商品[{}]发布成功，等待审核，ID={}", item.getTitle(), item.getId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateItem(Item item, Long operatorId) {
        // 先查询原商品，用于判断商品是否存在、操作者是否为卖家本人。
        Item exist = itemDao.findById(item.getId());
        if (exist == null) {
            throw BusinessException.notFound("商品");
        }
        if (!exist.getSellerId().equals(operatorId)) {
            throw BusinessException.forbidden("修改他人商品");
        }
        if (exist.getStatus() == 3 || exist.getStatus() == 4) {
            throw BusinessException.badRequest("已售出或已下架的商品无法修改");
        }
        // XML 中使用 <set> + <if>，只更新前端传入的非空字段。
        itemDao.update(item);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void takeDownItem(Long itemId, Long operatorId) {
        Item item = itemDao.findById(itemId);
        if (item == null) {
            throw BusinessException.notFound("商品");
        }
        if (!item.getSellerId().equals(operatorId)) {
            throw BusinessException.forbidden("下架他人商品");
        }
        if (item.getStatus() == 2) {
            throw BusinessException.badRequest("商品正在交易中，无法下架");
        }
        itemDao.updateStatus(itemId, 4);
        log.info("商品[{}]已下架", itemId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void addFavorite(Long userId, Long itemId) {
        // 检查商品是否存在
        Item item = itemDao.findById(itemId);
        if (item == null) {
            throw BusinessException.notFound("商品");
        }
        // 检查是否已收藏，避免同一个用户重复收藏同一件商品。
        if (favoriteDao.existsByUserIdAndItemId(userId, itemId) > 0) {
            throw BusinessException.badRequest("已收藏过该商品");
        }
        Favorite fav = new Favorite();
        fav.setUserId(userId);
        fav.setItemId(itemId);
        favoriteDao.insert(fav);
        // 收藏记录和商品收藏数必须一起成功，所以本方法开启事务。
        itemDao.increaseFavCount(itemId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void removeFavorite(Long userId, Long itemId) {
        int rows = favoriteDao.deleteByUserIdAndItemId(userId, itemId);
        if (rows > 0) {
            // 只有真的删除了收藏记录，才减少商品收藏数。
            itemDao.decreaseFavCount(itemId);
        }
    }
}
