package com.bazaar.vo;

import java.util.List;

/**
 * 分页结果封装
 * 技术点：
 * - 泛型 T 表示列表元素类型，PageResult<Item> 就是商品分页结果；
 * - total 用于前端计算总页数，list 是当前页的数据；
 * - 统一分页返回结构可以减少 Controller 中重复代码。
 *
 * @param <T> 数据类型
 */
public class PageResult<T> {

    /** 总记录数 */
    private long total;
    /** 当前页数据 */
    private List<T> list;

    public PageResult(long total, List<T> list) {
        this.total = total;
        this.list  = list;
    }

    public long getTotal() { return total; }
    public void setTotal(long total) { this.total = total; }

    public List<T> getList() { return list; }
    public void setList(List<T> list) { this.list = list; }
}
