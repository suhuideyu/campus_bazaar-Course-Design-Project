package com.bazaar.service.impl;

import com.bazaar.dao.UserDao;
import com.bazaar.domain.User;
import com.bazaar.exception.BusinessException;
import com.bazaar.service.UserService;
import com.bazaar.utils.MD5Utils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 用户业务实现类
 * 技术点：
 * - @Service 把当前类注册为 Spring Bean，Controller 可以通过 @Autowired 注入它；
 * - Service 层负责业务规则，例如参数校验、用户名唯一性、密码加密；
 * - DAO 层只负责数据库访问，Service 负责决定什么时候调用哪些 DAO 方法。
 */
@Service
public class UserServiceImpl implements UserService {

    /** SLF4J 日志门面：实际输出由 Spring Boot 默认日志实现完成 */
    private static final Logger log = LoggerFactory.getLogger(UserServiceImpl.class);

    @Autowired
    private UserDao userDao;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void register(User user) {
        System.out.println("后端收到的密码：" + user.getPassword());
        // 参数校验：在进入数据库前先拦截明显错误，减少无效 SQL。
        if (user.getUsername() == null || user.getUsername().trim().isEmpty()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        if (user.getPassword() == null || user.getPassword().length() < 6) {
            throw new IllegalArgumentException("密码长度不能少于6位");
        }
        if (user.getNickname() == null || user.getNickname().trim().isEmpty()) {
            throw new IllegalArgumentException("昵称不能为空");
        }

        // 用户名唯一性校验：先查再插入，真实项目还应在数据库 username 列加唯一索引。
        if (userDao.findByUsername(user.getUsername()) != null) {
            throw BusinessException.badRequest("用户名已被注册");
        }

        // 密码 MD5 加密：演示“明文密码不要直接入库”的思想。
        user.setPassword(MD5Utils.encrypt(user.getPassword()));

        userDao.insert(user);
        log.info("新用户注册成功：{}", user.getUsername());
    }

    @Override
    public User login(String username, String password) {
        if (username == null || password == null) {
            throw new IllegalArgumentException("用户名和密码不能为空");
        }

        // 登录流程：按用户名查用户 -> 检查状态 -> 比对密码摘要。
        User user = userDao.findByUsername(username);
        if (user == null) {
            throw BusinessException.badRequest("用户名或密码错误");
        }
        if (user.getStatus() == 0) {
            throw BusinessException.badRequest("账号已被禁用，请联系管理员");
        }
        if (!MD5Utils.matches(password, user.getPassword())) {
            throw BusinessException.badRequest("用户名或密码错误");
        }

        log.info("用户登录成功：{}", username);
        return user;
    }

    @Override
    public User getUserById(Long id) {
        User user = userDao.findById(id);
        if (user == null) {
            throw BusinessException.notFound("用户");
        }
        return user;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateUserInfo(User user) {
        // user.id 来自 Session 中的登录用户，避免前端传别人的 id 修改资料。
        userDao.update(user);
    }
}
