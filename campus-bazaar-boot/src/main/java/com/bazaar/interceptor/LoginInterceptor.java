package com.bazaar.interceptor;

import com.bazaar.domain.User;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.Map;

/**
 * 登录拦截器：检查 Session 中是否存在登录用户
 * 技术点：
 * - HandlerInterceptor 是 Spring MVC 的拦截器接口；
 * - preHandle 在 Controller 方法执行前调用；
 * - 返回 true 表示继续执行 Controller，返回 false 表示请求到此结束；
 * - 这里使用 HttpSession 保存登录状态，适合传统教学项目理解会话机制。
 */
public class LoginInterceptor implements HandlerInterceptor {

    public static final String SESSION_USER_KEY = "loginUser";

    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {

        // 从服务端 Session 中读取登录用户。Session ID 通常由浏览器 Cookie 保存。
        User loginUser = (User) request.getSession().getAttribute(SESSION_USER_KEY);
        if (loginUser != null) {
            return true; // 已登录，放行
        }

        // 未登录：返回 401 JSON。这里没有进入 Controller，所以需要手动写响应。
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType("application/json;charset=UTF-8");

        Map<String, Object> result = new HashMap<>();
        result.put("code", 401);
        result.put("message", "请先登录");
        result.put("data", null);

        response.getWriter().write(MAPPER.writeValueAsString(result));
        return false;
    }
}
