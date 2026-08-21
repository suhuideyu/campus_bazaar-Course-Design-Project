package com.bazaar.controller;

import com.bazaar.common.Result;
import com.bazaar.domain.Order;
import com.bazaar.domain.User;
import com.bazaar.interceptor.LoginInterceptor;
import com.bazaar.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.List;
import java.util.Map;

/**
 * 订单相关接口
 * 基础路径：/api/orders（全部需要登录）
 * 技术点：
 * - 订单接口涉及“商品状态 + 订单状态”的连续修改，真正的一致性保证在 Service 层事务中完成；
 * - Controller 只做请求参数转换，例如把 JSON 里的 itemId 转成 Long；
 * - 当前登录用户从 Session 中取得，避免前端伪造 buyerId/sellerId。
 */
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @Autowired
    private OrderService orderService;

    /**
     * 提交订单
     * POST /api/orders
     * Body: {"itemId":1,"message":"方便的话图书馆见","meetPlace":"图书馆门口"}
     */
    @PostMapping
    public Result<Order> submit(@RequestBody Map<String, Object> params,
                                 HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        Long   itemId    = Long.valueOf(params.get("itemId").toString());
        String message   = (String) params.get("message");
        String meetPlace = (String) params.get("meetPlace");

        Order order = orderService.submitOrder(itemId, loginUser.getId(), message, meetPlace);
        return Result.success("订单提交成功，等待卖家确认", order);
    }

    /**
     * 我买到的订单
     * GET /api/orders/buy
     */
    @GetMapping("/buy")
    public Result<List<Order>> myBuyOrders(HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        return Result.success(orderService.getMyBuyOrders(loginUser.getId()));
    }

    /**
     * 我卖出的订单
     * GET /api/orders/sell
     */
    @GetMapping("/sell")
    public Result<List<Order>> mySellOrders(HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        return Result.success(orderService.getMySellOrders(loginUser.getId()));
    }

    /**
     * 卖家确认订单
     * PUT /api/orders/{id}/confirm
     */
    @PutMapping("/{id}/confirm")
    public Result<Void> confirm(@PathVariable Long id, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        orderService.confirmOrder(id, loginUser.getId());
        return Result.success("已确认订单", null);
    }

    /**
     * 买家确认完成交易
     * PUT /api/orders/{id}/finish
     */
    @PutMapping("/{id}/finish")
    public Result<Void> finish(@PathVariable Long id, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        orderService.finishOrder(id, loginUser.getId());
        return Result.success("交易完成！", null);
    }

    /**
     * 取消订单（买卖家均可）
     * PUT /api/orders/{id}/cancel
     */
    @PutMapping("/{id}/cancel")
    public Result<Void> cancel(@PathVariable Long id, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        orderService.cancelOrder(id, loginUser.getId());
        return Result.success("订单已取消", null);
    }

    /**
     * 查看商品关联的订单（仅买卖家可查看）
     * GET /api/orders/item/{itemId}
     */
    @GetMapping("/item/{itemId}")
    public Result<Order> getByItem(@PathVariable Long itemId, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        Order order = orderService.getOrderByItemId(itemId, loginUser.getId());
        return Result.success(order);
    }
}
