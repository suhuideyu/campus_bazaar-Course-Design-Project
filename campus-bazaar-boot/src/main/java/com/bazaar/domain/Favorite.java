package com.bazaar.domain;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

/**
 * 收藏实体，对应 cb_favorite 表
 * 技术点：
 * - 收藏是“用户-商品”的关联关系，userId 指向用户，itemId 指向商品；
 * - itemTitle/itemPrice 等字段来自关联查询，方便前端直接展示收藏列表。
 */
public class Favorite {

    private Long id;
    private Long userId;
    private Long itemId;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date createdAt;

    // 关联查询附加字段
    private String itemTitle;
    private String itemImages;
    private String itemPrice;
    private Integer itemStatus;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }

    public Long getItemId() { return itemId; }
    public void setItemId(Long itemId) { this.itemId = itemId; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public String getItemTitle() { return itemTitle; }
    public void setItemTitle(String itemTitle) { this.itemTitle = itemTitle; }

    public String getItemImages() { return itemImages; }
    public void setItemImages(String itemImages) { this.itemImages = itemImages; }

    public String getItemPrice() { return itemPrice; }
    public void setItemPrice(String itemPrice) { this.itemPrice = itemPrice; }

    public Integer getItemStatus() { return itemStatus; }
    public void setItemStatus(Integer itemStatus) { this.itemStatus = itemStatus; }
}
