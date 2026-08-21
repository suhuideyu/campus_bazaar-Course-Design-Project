package com.bazaar.service;

import com.bazaar.domain.User;

/**
 * 用户业务接口
 * 技术点：
 * - Service 层定义“业务能力”，Controller 不直接关心 SQL 怎么写；
 * - 接口和实现类分离，便于后续替换实现、做单元测试或扩展业务。
 */
public interface UserService {

    /** 注册（用户名唯一性校验 + 密码加密） */
    void register(User user);

    /** 登录（校验密码，返回用户对象） */
    User login(String username, String password);

    User getUserById(Long id);

    void updateUserInfo(User user);
}