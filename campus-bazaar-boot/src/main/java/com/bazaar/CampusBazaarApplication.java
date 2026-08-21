package com.bazaar;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * 校园集市 —— SpringBoot 启动类
 *
 * @SpringBootApplication = @SpringBootConfiguration + @EnableAutoConfiguration + @ComponentScan
 *   - @SpringBootConfiguration：标识这是SpringBoot配置类
 *   - @EnableAutoConfiguration：开启自动配置（SpringBoot的核心！）
 *   - @ComponentScan：扫描当前包及子包下的所有组件
 */
@SpringBootApplication
@MapperScan("com.bazaar.dao")           // 扫描Mapper接口（替代 MapperScannerConfigurer）
@EnableTransactionManagement            // 开启事务管理（替代 <tx:annotation-driven/>）
public class CampusBazaarApplication {

    public static void main(String[] args) {
        // SpringApplication.run 会创建 Spring 容器、启动内置 Tomcat、加载 application.yml 配置。
        SpringApplication.run(CampusBazaarApplication.class, args);
        System.out.println("=================================================");
        System.out.println("  校园集市启动成功！");
        System.out.println("  接口地址：http://localhost:8080");
        System.out.println("  分类列表：http://localhost:8080/api/categories");
        System.out.println("  商品列表：http://localhost:8080/api/items");
        System.out.println("=================================================");
    }
}