package com.bazaar.dao;

import java.util.List;
import com.bazaar.domain.User;
import org.apache.ibatis.annotations.Param;

/**
 * 用户 DAO 接口
 * 技术点：
 * - DAO(Data Access Object) 层只负责数据库访问，不写业务规则；
 * - 本接口没有实现类，MyBatis 会根据 UserDao.xml 在运行时生成代理对象；
 * - 方法名需要和 mapper XML 中的 select/insert/update 标签 id 保持一致；
 * - 多个简单参数使用 @Param 起别名，XML 中才能通过 #{id}、#{delta} 取值。
 */
public interface UserDao {

    /** 根据主键查询用户 */
    User findById(Long id);

    /** 根据用户名查询用户，注册和登录都会用到 */
    User findByUsername(String username);

    /** 插入用户，主键回填到 user.id */
    int insert(User user);

    /** 动态更新用户资料，只修改 XML 中判断为非空的字段 */
    int update(User user);

    /** 调整信用分，delta 可为正负，结果限制在 [0, 200] */
    int updateCreditScore(@Param("id") Long id, @Param("delta") int delta);

    /** 修改账号状态：0=禁用，1=正常 */
    int updateStatus(@Param("id") Long id, @Param("status") Integer status);

    /** 分页查询所有用户 */
    List<User> findAll(@Param("offset") int offset, @Param("limit") int limit);

    /** 用户总数 */
    long countAll();
}
