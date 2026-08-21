package com.bazaar.service;

import com.bazaar.domain.Review;

public interface ReviewService {

    Review getByItemId(Long itemId);

    boolean canReview(Long orderId, Long userId);

    Review createReview(Long orderId, Long reviewerId, Integer score, String content);
}
