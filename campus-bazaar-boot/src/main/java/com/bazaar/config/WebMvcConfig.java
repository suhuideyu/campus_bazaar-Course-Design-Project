package com.bazaar.config;

import com.bazaar.interceptor.AdminInterceptor;
import com.bazaar.interceptor.LoginInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * SpringMVC 配置类（替代 SSM 的 spring-mvc.xml）
 * 技术点：
 * - @Configuration：把当前类交给 Spring 容器管理，启动时自动读取这里的配置。
 * - WebMvcConfigurer：Spring MVC 提供的扩展接口，可以配置拦截器、跨域、资源映射等。
 * - HandlerInterceptor：在请求进入 Controller 之前做统一处理，常用于登录校验。
 */
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 注册自定义登录拦截器。匹配 /api/** 的请求，再排除公开接口。
        registry.addInterceptor(new LoginInterceptor())
                .addPathPatterns("/api/**")
                .excludePathPatterns(
                        "/api/users/login",
                        "/api/users/register",
                        "/api/items",
                        "/api/items/{id:\\d+}",
                        "/api/items/seller/**",
                        "/api/categories",
                        "/api/comments/item/**",
                        "/api/reviews/item/**"
                );
        // 管理员拦截器：拦截 /api/admin/**，需要管理员角色
        registry.addInterceptor(new AdminInterceptor())
                .addPathPatterns("/api/admin/**");
    }
}
