package com.bazaar.vo;

/**
 * 商品查询条件对象
 * VO = Value Object，专门用于传递查询参数
 */
public class ItemQueryVO {
    private Integer categoryId;  // 分类ID，null表示不限
    private String keyword;      // 关键词搜索标题
    private Integer status;      // 商品状态，null表示不限
    private String orderBy;      // 排序：price_asc/price_desc/newest/hottest
    private Integer pageNum=1;     // 当前页（从1开始）
    private Integer pageSize=10;    // 每页条数
    private Boolean adminMode;     // 管理员模式，true时不强制过滤status=1

    //供 MyBatis 分页使用：第 1 页 offset=0，第 2 页 offset=pageSize
    public int getOffset() {
        return (pageNum - 1) * pageSize;
    }

    // ===================== getter & setter =====================
    public Integer getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Integer categoryId) {
        this.categoryId = categoryId;
    }

    public String getKeyword() {
        return keyword;
    }

    public void setKeyword(String keyword) {
        this.keyword = keyword;
    }

    public Integer getStatus() {
        return status;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }

    public String getOrderBy() {
        return orderBy;
    }

    public void setOrderBy(String orderBy) {
        this.orderBy = orderBy;
    }

    public Integer getPageNum() {
        return pageNum;
    }

    public void setPageNum(Integer pageNum) {
        this.pageNum = pageNum;
    }

    public Integer getPageSize() {
        return pageSize;
    }

    public void setPageSize(Integer pageSize) {
        this.pageSize = pageSize;
    }

    public Boolean getAdminMode() {
        return adminMode;
    }

    public void setAdminMode(Boolean adminMode) {
        this.adminMode = adminMode;
    }
}