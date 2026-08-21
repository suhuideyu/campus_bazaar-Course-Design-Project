package com.bazaar.dao;

import com.bazaar.domain.Review;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface ReviewDao {

    Review findByOrderId(Long orderId);

    Integer existsByOrderId(Long orderId);

    List<Review> findByItemId(@Param("itemId") Long itemId);

    int insert(Review review);
}
