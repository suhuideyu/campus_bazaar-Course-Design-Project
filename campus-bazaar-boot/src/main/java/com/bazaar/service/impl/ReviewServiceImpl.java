package com.bazaar.service.impl;

import com.bazaar.dao.OrderDao;
import com.bazaar.dao.ReviewDao;
import com.bazaar.domain.Order;
import com.bazaar.domain.Review;
import com.bazaar.exception.BusinessException;
import com.bazaar.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ReviewServiceImpl implements ReviewService {

    @Autowired
    private ReviewDao reviewDao;

    @Autowired
    private OrderDao orderDao;

    @Override
    public Review getByItemId(Long itemId) {
        List<Review> list = reviewDao.findByItemId(itemId);
        return list.isEmpty() ? null : list.get(0);
    }

    @Override
    public boolean canReview(Long orderId, Long userId) {
        if (reviewDao.existsByOrderId(orderId) > 0) {
            return false;
        }
        Order order = orderDao.findById(orderId);
        if (order == null) {
            return false;
        }
        // Only buyer can review, and only when order is completed
        return order.getStatus() == 2 && order.getBuyerId().equals(userId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Review createReview(Long orderId, Long reviewerId, Integer score, String content) {
        if (score == null || score < 1 || score > 5) {
            throw new IllegalArgumentException("评分必须在1-5之间");
        }
        if (!canReview(orderId, reviewerId)) {
            throw BusinessException.badRequest("无法评价该订单");
        }
        Order order = orderDao.findById(orderId);

        Review review = new Review();
        review.setOrderId(orderId);
        review.setReviewerId(reviewerId);
        review.setRevieweeId(order.getSellerId());
        review.setScore(score);
        review.setContent(content != null ? content.trim() : null);
        reviewDao.insert(review);
        return review;
    }
}
