package com.bazaar.controller;

import com.bazaar.common.Result;
import com.bazaar.domain.Item;
import com.bazaar.domain.User;
import com.bazaar.service.AdminService;
import com.bazaar.vo.PageResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    @Autowired
    private AdminService adminService;

    /**
     * 获取用户列表
     * GET /api/admin/users?page=1&size=10
     */
    @GetMapping("/users")
    public Result<PageResult<User>> listUsers(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        return Result.success(adminService.listUsers(page, size));
    }

    /**
     * 修改用户状态
     * PUT /api/admin/users/{id}/status
     * Body: {"status": 0}  0=禁用, 1=正常
     */
    @PutMapping("/users/{id}/status")
    public Result<Void> updateUserStatus(@PathVariable Long id, @RequestBody Map<String, Integer> body) {
        Integer status = body.get("status");
        adminService.updateUserStatus(id, status);
        String msg = status == 1 ? "用户已启用" : "用户已禁用";
        return Result.success(msg, null);
    }

    /**
     * 获取商品列表（含待审核）
     * GET /api/admin/items?page=1&size=10&status=0&keyword=
     */
    @GetMapping("/items")
    public Result<PageResult<Item>> listItems(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Integer status,
            @RequestParam(required = false) String keyword) {
        return Result.success(adminService.listItems(page, size, status, keyword));
    }

    /**
     * 修改商品状态（审核通过/下架等）
     * PUT /api/admin/items/{id}/status
     * Body: {"status": 1}  0=待审核, 1=在售, 2=锁定, 3=已售, 4=下架
     */
    @PutMapping("/items/{id}/status")
    public Result<Void> updateItemStatus(@PathVariable Long id, @RequestBody Map<String, Integer> body) {
        Integer status = body.get("status");
        adminService.updateItemStatus(id, status);
        return Result.success("商品状态已更新", null);
    }
}
