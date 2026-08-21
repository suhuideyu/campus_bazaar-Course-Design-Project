package com.bazaar.dao;

import com.bazaar.domain.Category;

import java.util.List;

/**
 * 商品分类 DAO 接口
 * 技术点：
 * - 分类数据通常变化少，接口以简单查询为主；
 * - Spring 启动类上的 @MapperScan 会扫描本包，让 MyBatis 创建该接口的代理对象。
 */
public interface CategoryDao {

    /** 查询全部分类，页面下拉框或分类导航使用 */
    List<Category> findAll();

    /** 根据分类 ID 查询单个分类 */
    Category findById(Integer id);
}
