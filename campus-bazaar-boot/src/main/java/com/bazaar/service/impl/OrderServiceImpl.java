package com.bazaar.service.impl;

import com.bazaar.dao.ItemDao;
import com.bazaar.dao.OrderDao;
import com.bazaar.dao.UserDao;
import com.bazaar.domain.Item;
import com.bazaar.domain.Order;
import com.bazaar.exception.BusinessException;
import com.bazaar.service.OrderService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Random;

/**
 * 订单业务实现类
 * 技术点：
 * - 订单是本项目里最典型的事务场景：订单状态和商品状态要一起变化；
 * - @Transactional 保证一个业务方法中的多条 SQL 要么全部成功，要么全部回滚；
 * - 买家/卖家身份校验放在 Service 层，防止前端伪造参数绕过权限。
 */
@Service
public class OrderServiceImpl implements OrderService {

    private static final Logger log = LoggerFactory.getLogger(OrderServiceImpl.class);

    @Autowired
    private OrderDao orderDao;
    @Autowired
    private ItemDao  itemDao;
    @Autowired
    private UserDao  userDao;

    /**
     * 提交订单
     * 事务保证：商品锁定 + 订单创建 原子完成
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public Order submitOrder(Long itemId, Long buyerId, String message, String meetPlace) {

        // ① 查商品：提交订单前必须拿到商品当前状态和卖家 ID。
        Item item = itemDao.findById(itemId);
        if (item == null) {
            throw BusinessException.notFound("商品");
        }
        // ② 业务校验：只有在售商品可购买，且不能购买自己发布的商品。
        if (item.getStatus() != 1) {
            throw BusinessException.badRequest("该商品当前不可购买（可能已下架或被他人锁定）");
        }
        if (item.getSellerId().equals(buyerId)) {
            throw BusinessException.badRequest("不能购买自己发布的商品");
        }

        // ③ 锁定商品（status -> 2：锁定中），防止同一商品被继续购买。
        int rows = itemDao.updateStatus(itemId, 2);
        if (rows == 0) {
            throw BusinessException.badRequest("商品状态更新失败，请重试");
        }

        // ④ 创建订单：保存商品、买家、卖家、价格、留言、见面地点等交易信息。
        Order order = new Order();
        order.setOrderNo(generateOrderNo());
        order.setItemId(itemId);
        order.setBuyerId(buyerId);
        order.setSellerId(item.getSellerId());
        order.setPrice(item.getPrice());
        order.setMessage(message);
        order.setMeetPlace(meetPlace);
        order.setStatus(0); // 待卖家确认

        orderDao.insert(order);
        log.info("订单[{}]创建成功，商品[{}]已锁定", order.getOrderNo(), itemId);
        return order;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void confirmOrder(Long orderId, Long sellerId) {
        Order order = getOrderAndCheck(orderId);
        // 只有订单中的卖家本人才能确认订单。
        if (!order.getSellerId().equals(sellerId)) {
            throw BusinessException.forbidden("操作他人订单");
        }
        if (order.getStatus() != 0) {
            throw BusinessException.badRequest("订单状态不正确，无法确认");
        }
        orderDao.updateStatus(orderId, 1);
        log.info("订单[{}]已被卖家确认", orderId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void finishOrder(Long orderId, Long buyerId) {
        Order order = getOrderAndCheck(orderId);
        // 只有买家本人能确认交易完成。
        if (!order.getBuyerId().equals(buyerId)) {
            throw BusinessException.forbidden("操作他人订单");
        }
        if (order.getStatus() != 1) {
            throw BusinessException.badRequest("订单尚未被卖家确认，无法完成");
        }

        // 订单 -> 已完成
        orderDao.updateStatus(orderId, 2);
        // 商品 -> 已售出
        itemDao.updateStatus(order.getItemId(), 3);
        // 卖家信用 +2：演示一个业务动作可以影响多张表。
        userDao.updateCreditScore(order.getSellerId(), 2);
        log.info("订单[{}]交易完成，卖家[{}]信用+2", orderId, order.getSellerId());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void cancelOrder(Long orderId, Long userId) {
        Order order = getOrderAndCheck(orderId);

        boolean isBuyer  = order.getBuyerId().equals(userId);
        boolean isSeller = order.getSellerId().equals(userId);
        if (!isBuyer && !isSeller) {
            throw BusinessException.forbidden("取消此订单");
        }
        if (order.getStatus() >= 2) {
            throw BusinessException.badRequest("交易已完成或已取消，无法再次取消");
        }

        // 订单 -> 已取消
        orderDao.updateStatus(orderId, 3);
        // 商品解锁 -> 在售
        itemDao.updateStatus(order.getItemId(), 1);
        log.info("订单[{}]已取消，商品[{}]恢复在售", orderId, order.getItemId());
    }

    @Override
    public List<Order> getMyBuyOrders(Long buyerId) {
        return orderDao.findByBuyerId(buyerId);
    }

    @Override
    public List<Order> getMySellOrders(Long sellerId) {
        return orderDao.findBySellerId(sellerId);
    }

    @Override
    public Order getOrderByItemId(Long itemId, Long userId) {
        // Find the active (not cancelled) order for this item
        Order order = orderDao.findByItemIdAndStatus(itemId, 0);
        if (order == null) {
            order = orderDao.findByItemIdAndStatus(itemId, 1);
        }
        if (order == null) {
            return null;
        }
        // Only buyer or seller can see the order
        if (order.getBuyerId().equals(userId) || order.getSellerId().equals(userId)) {
            return order;
        }
        return null;
    }

    // ===== 私有辅助方法：只给本类内部复用，不暴露给 Controller =====

    private Order getOrderAndCheck(Long orderId) {
        Order order = orderDao.findById(orderId);
        if (order == null) {
            throw BusinessException.notFound("订单");
        }
        return order;
    }

    /** 生成订单号：CB + yyyyMMddHHmmss + 4位随机数；教学项目够用，真实项目需考虑高并发唯一性。 */
    private String generateOrderNo() {
        String time   = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss"));
        int    suffix = new Random().nextInt(9000) + 1000;
        return "CB" + time + suffix;
    }
}
