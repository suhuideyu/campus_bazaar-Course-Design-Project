package com.bazaar.controller;

import com.bazaar.common.Result;
import com.bazaar.dao.CategoryDao;
import com.bazaar.domain.Category;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 商品分类接口（公开，无需登录）
 * 技术点：
 * - 简单查询接口可以直接调用 DAO；
 * - 如果后续出现复杂业务规则，再抽出 CategoryService 层。
 */
@RestController
@RequestMapping("/api/categories")
public class CategoryController {

    @Autowired
    private CategoryDao categoryDao;

    /**
     * 获取所有分类
     * GET /api/categories
     */
    @GetMapping
    public Result<List<Category>> list() {
        return Result.success(categoryDao.findAll());
    }
}
