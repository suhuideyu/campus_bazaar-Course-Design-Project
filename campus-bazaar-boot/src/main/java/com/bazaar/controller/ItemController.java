package com.bazaar.controller;

import com.bazaar.common.Result;
import com.bazaar.domain.Item;
import com.bazaar.domain.User;
import com.bazaar.interceptor.LoginInterceptor;
import com.bazaar.service.ItemService;
import com.bazaar.vo.ItemQueryVO;
import com.bazaar.vo.PageResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.List;

/**
 * 商品相关接口
 * 基础路径：/api/items
 * 技术点：
 * - 这是 Spring MVC 的 Controller 层，负责把 HTTP 请求映射到 Java 方法；
 * - @GetMapping/@PostMapping/@PutMapping/@DeleteMapping 分别对应 REST 风格的查询、新增、修改、删除；
 * - @PathVariable 读取 URL 路径中的变量，如 /api/items/1 里的 1；
 * - 普通对象参数 ItemQueryVO 会自动接收 query string 参数，如 pageNum=1&pageSize=10。
 */
@RestController
@RequestMapping("/api/items")
public class ItemController {

    @Autowired
    private ItemService itemService;

    /**
     * 商品列表（公开，不需要登录）
     * GET /api/items?categoryId=1&keyword=数学&orderBy=price_asc&pageNum=1&pageSize=10
     */
    @GetMapping
    public Result<PageResult<Item>> list(ItemQueryVO query) {
        PageResult<Item> result = itemService.getItemList(query);
        return Result.success(result);
    }

    /**
     * 商品详情（公开）
     * GET /api/items/{id}
     */
    @GetMapping("/{id}")
    public Result<Item> detail(@PathVariable Long id) {
        return Result.success(itemService.getItemDetail(id));
    }

    /**
     * 发布商品（需登录）
     * POST /api/items
     */
    @PostMapping
    public Result<Item> publish(@RequestBody Item item, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        item.setSellerId(loginUser.getId());
        itemService.publishItem(item);
        return Result.success("发布成功，等待审核", item);
    }

    /**
     * 修改商品（需登录，且是卖家本人）
     * PUT /api/items/{id}
     */
    @PutMapping("/{id}")
    public Result<Void> update(@PathVariable Long id,
                               @RequestBody Item item,
                               HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        item.setId(id);
        itemService.updateItem(item, loginUser.getId());
        return Result.success("修改成功", null);
    }

    /**
     * 下架商品（需登录，且是卖家本人）
     * DELETE /api/items/{id}
     */
    @DeleteMapping("/{id}")
    public Result<Void> takeDown(@PathVariable Long id, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        itemService.takeDownItem(id, loginUser.getId());
        return Result.success("商品已下架", null);
    }

    /**
     * 收藏商品（需登录）
     * POST /api/items/{id}/favorite
     */
    @PostMapping("/{id}/favorite")
    public Result<Void> addFavorite(@PathVariable Long id, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        itemService.addFavorite(loginUser.getId(), id);
        return Result.success("收藏成功", null);
    }

    /**
     * 取消收藏（需登录）
     * DELETE /api/items/{id}/favorite
     */
    @DeleteMapping("/{id}/favorite")
    public Result<Void> removeFavorite(@PathVariable Long id, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        itemService.removeFavorite(loginUser.getId(), id);
        return Result.success("已取消收藏", null);
    }

    /**
     * 查看某卖家发布的商品（公开）
     * GET /api/items/seller/{sellerId}
     */
    @GetMapping("/seller/{sellerId}")
    public Result<List<Item>> bySeller(@PathVariable Long sellerId) {
        return Result.success(itemService.getItemsBySeller(sellerId));
    }

    /**
     * 查看某卖家发布的在售商品（公开，仅status=1）
     * GET /api/items/seller/{sellerId}/onsale
     */
    @GetMapping("/seller/{sellerId}/onsale")
    public Result<List<Item>> bySellerOnSale(@PathVariable Long sellerId) {
        return Result.success(itemService.getItemsBySellerOnSale(sellerId));
    }
}
