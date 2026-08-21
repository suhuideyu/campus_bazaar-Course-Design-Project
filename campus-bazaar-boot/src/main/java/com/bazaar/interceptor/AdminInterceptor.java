package com.bazaar.interceptor;

import com.bazaar.domain.User;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.Map;

/**
 * 管理员拦截器：检查登录用户是否拥有管理员角色
 */
public class AdminInterceptor implements HandlerInterceptor {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {

        User loginUser = (User) request.getSession().getAttribute(LoginInterceptor.SESSION_USER_KEY);

        if (loginUser == null) {
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.setContentType("application/json;charset=UTF-8");

            Map<String, Object> result = new HashMap<>();
            result.put("code", 401);
            result.put("message", "请先登录");
            result.put("data", null);

            response.getWriter().write(MAPPER.writeValueAsString(result));
            return false;
        }

        if (loginUser.getRole() == null || loginUser.getRole() != 1) {
            response.setStatus(HttpServletResponse.SC_FORBIDDEN);
            response.setContentType("application/json;charset=UTF-8");

            Map<String, Object> result = new HashMap<>();
            result.put("code", 403);
            result.put("message", "无管理员权限");
            result.put("data", null);

            response.getWriter().write(MAPPER.writeValueAsString(result));
            return false;
        }

        return true;
    }
}
