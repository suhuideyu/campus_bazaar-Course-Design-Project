package com.bazaar.domain;

/**
 * 商品分类实体，对应 cb_category 表
 * 技术点：
 * - 分类属于基础字典数据，常用于商品发布表单和商品列表筛选；
 * - sort 字段用于控制前端显示顺序，不建议依赖数据库默认顺序。
 */
public class Category {

    private Integer id;
    private String name;
    private String icon;
    private Integer sort;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getIcon() { return icon; }
    public void setIcon(String icon) { this.icon = icon; }

    public Integer getSort() { return sort; }
    public void setSort(Integer sort) { this.sort = sort; }

    @Override
    public String toString() {
        return "Category{id=" + id + ", name='" + name + "'}";
    }
}
