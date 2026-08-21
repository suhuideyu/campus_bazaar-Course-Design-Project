package com.bazaar.dao;

import com.bazaar.domain.Order;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface OrderDao {

    // 根据订单ID查询订单
    Order findById(@Param("id") Long id);

    // 根据买家ID查询我的订单列表
    List<Order> findByBuyerId(@Param("buyerId") Long buyerId);

    // 根据卖家ID查询我的卖出订单
    List<Order> findBySellerId(@Param("sellerId") Long sellerId);

    // 插入新订单
    int insert(Order order);

    // 更新订单状态
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);

    // 根据商品ID和订单状态查询订单
    Order findByItemIdAndStatus(@Param("itemId") Long itemId, @Param("status") Integer status);
}