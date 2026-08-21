package com.bazaar.controller;

import com.bazaar.common.Result;
import com.bazaar.dao.FavoriteDao;
import com.bazaar.domain.Favorite;
import com.bazaar.domain.User;
import com.bazaar.interceptor.LoginInterceptor;
import com.bazaar.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.List;
import java.util.Map;

/**
 * 用户相关接口
 * 基础路径：/api/users
 * 技术点：
 * - @RestController = @Controller + @ResponseBody，返回值直接转 JSON；
 * - @RequestMapping 声明本控制器的统一访问前缀；
 * - @Autowired 从 Spring 容器中注入 Service/DAO 对象；
 * - Controller 层只负责接收请求、取参数、返回结果，核心业务放到 Service 层。
 */
@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private FavoriteDao favoriteDao;

    /**
     * 注册
     * POST /api/users/register
     * Body: {"username":"","password":"","nickname":"","phone":"","school":""}
     * @RequestBody 表示从请求体 JSON 中读取数据，并转换为 User 对象。
     */
    @PostMapping("/register")
    public Result<Void> register(@RequestBody User user) {
        userService.register(user);
        return Result.success("注册成功", null);
    }

    /**
     * 登录
     * POST /api/users/login
     * Body: {"username":"","password":""}
     * HttpSession 用于在服务端保存登录用户信息，后续请求可通过 Session 判断是否已登录。
     */
    @PostMapping("/login")
    public Result<User> login(@RequestBody Map<String, String> params, HttpSession session) {
        String username = params.get("username");
        String password = params.get("password");
        User user = userService.login(username, password);
        session.setAttribute(LoginInterceptor.SESSION_USER_KEY, user);
        user.setPassword(null); // 不返回密码
        return Result.success("登录成功", user);
    }

    /**
     * 退出登录
     * POST /api/users/logout
     */
    @PostMapping("/logout")
    public Result<Void> logout(HttpSession session) {
        session.removeAttribute(LoginInterceptor.SESSION_USER_KEY);
        return Result.success("已退出登录", null);
    }

    /**
     * 获取当前登录用户信息
     * GET /api/users/me
     */
    @GetMapping("/me")
    public Result<User> me(HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        loginUser.setPassword(null);
        return Result.success(loginUser);
    }

    /**
     * 获取指定用户公开信息
     * GET /api/users/{id}
     */
    @GetMapping("/{id}")
    public Result<User> getUserInfo(@PathVariable Long id) {
        User user = userService.getUserById(id);
        user.setPassword(null);
        return Result.success(user);
    }

    /**
     * 修改个人信息
     * PUT /api/users/me
     */
    @PutMapping("/me")
    public Result<Void> updateMyInfo(@RequestBody User user, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        user.setId(loginUser.getId());
        userService.updateUserInfo(user);
        return Result.success("修改成功", null);
    }

    /**
     * 查看我的收藏列表
     * GET /api/users/me/favorites
     */
    @GetMapping("/me/favorites")
    public Result<List<Favorite>> myFavorites(HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        List<Favorite> list = favoriteDao.findByUserId(loginUser.getId());
        return Result.success(list);
    }
}
