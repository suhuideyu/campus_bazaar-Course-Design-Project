package com.bazaar.controller;

import com.bazaar.common.Result;
import com.bazaar.domain.Review;
import com.bazaar.domain.User;
import com.bazaar.interceptor.LoginInterceptor;
import com.bazaar.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.Map;

@RestController
@RequestMapping("/api/reviews")
public class ReviewController {

    @Autowired
    private ReviewService reviewService;

    /**
     * 获取商品的评价
     * GET /api/reviews/item/{itemId}
     */
    @GetMapping("/item/{itemId}")
    public Result<Review> getByItem(@PathVariable Long itemId) {
        Review review = reviewService.getByItemId(itemId);
        return Result.success(review);
    }

    /**
     * 检查是否可以评价
     * GET /api/reviews/check/{orderId}
     */
    @GetMapping("/check/{orderId}")
    public Result<Boolean> checkCanReview(@PathVariable Long orderId, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        boolean can = reviewService.canReview(orderId, loginUser.getId());
        return Result.success(can);
    }

    /**
     * 提交评价
     * POST /api/reviews
     * Body: {"orderId": 1, "score": 5, "content": "..."}
     */
    @PostMapping
    public Result<Review> create(@RequestBody Map<String, Object> body, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        Long orderId = Long.valueOf(body.get("orderId").toString());
        Integer score = (Integer) body.get("score");
        String content = (String) body.get("content");
        Review review = reviewService.createReview(orderId, loginUser.getId(), score, content);
        return Result.success("评价成功", review);
    }
}
