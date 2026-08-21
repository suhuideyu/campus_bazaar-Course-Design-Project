package com.bazaar.service;

import com.bazaar.domain.Order;

import java.util.List;

/**
 * 订单业务接口
 * 技术点：
 * - 订单业务通常需要事务，因为一次操作会同时影响订单表、商品表、用户表；
 * - 接口中的方法名表达业务动作，比直接暴露 update/insert 更容易理解。
 */
public interface OrderService {

    /** 提交订单（含事务：锁定商品 + 创建订单） */
    Order submitOrder(Long itemId, Long buyerId, String message, String meetPlace);

    /** 卖家确认订单 */
    void confirmOrder(Long orderId, Long sellerId);

    /** 买家确认完成交易（商品→已售，卖家信用+2） */
    void finishOrder(Long orderId, Long buyerId);

    /** 取消订单（买卖家均可，商品解锁→在售） */
    void cancelOrder(Long orderId, Long userId);

    List<Order> getMyBuyOrders(Long buyerId);

    List<Order> getMySellOrders(Long sellerId);

    Order getOrderByItemId(Long itemId, Long userId);
}
