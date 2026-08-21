package com.bazaar.domain;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.math.BigDecimal;
import java.util.Date;

/**
 * 商品实体，对应 cb_item 表
 * 技术点：
 * - BigDecimal 用来表示金额，比 double 更适合价格计算；
 * - createdAt/updatedAt 使用 @JsonFormat 控制接口返回的时间格式；
 * - sellerNickname/categoryName 等字段不是 cb_item 表列，而是多表 JOIN 查询后的展示字段。
 */
public class Item {

    private Long id;
    private Long sellerId;
    private Integer categoryId;
    private String title;
    private String description;
    private String images;
    private BigDecimal price;
    private BigDecimal originalPrice;
    /**
     * 成色：1=几乎全新，2=轻微使用，3=正常使用，4=明显使用，5=大量使用痕迹
     */
    private Integer conditionLevel;
    /**
     * 状态：0=待审核，1=在售，2=锁定中，3=已售出，4=已下架
     */
    private Integer status;
    private Integer viewCount;
    private Integer favCount;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date createdAt;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date updatedAt;

    // ===== 多表关联查询时的附加字段（不在数据库列中）=====
    private String sellerNickname;
    private String sellerAvatar;
    private String categoryName;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getSellerId() { return sellerId; }
    public void setSellerId(Long sellerId) { this.sellerId = sellerId; }

    public Integer getCategoryId() { return categoryId; }
    public void setCategoryId(Integer categoryId) { this.categoryId = categoryId; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getImages() { return images; }
    public void setImages(String images) { this.images = images; }

    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }

    public BigDecimal getOriginalPrice() { return originalPrice; }
    public void setOriginalPrice(BigDecimal originalPrice) { this.originalPrice = originalPrice; }

    public Integer getConditionLevel() { return conditionLevel; }
    public void setConditionLevel(Integer conditionLevel) { this.conditionLevel = conditionLevel; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Integer getViewCount() { return viewCount; }
    public void setViewCount(Integer viewCount) { this.viewCount = viewCount; }

    public Integer getFavCount() { return favCount; }
    public void setFavCount(Integer favCount) { this.favCount = favCount; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    public String getSellerNickname() { return sellerNickname; }
    public void setSellerNickname(String sellerNickname) { this.sellerNickname = sellerNickname; }

    public String getSellerAvatar() { return sellerAvatar; }
    public void setSellerAvatar(String sellerAvatar) { this.sellerAvatar = sellerAvatar; }

    public String getCategoryName() { return categoryName; }
    public void setCategoryName(String categoryName) { this.categoryName = categoryName; }

    @Override
    public String toString() {
        return "Item{id=" + id + ", title='" + title + "', price=" + price + ", status=" + status + "}";
    }
}
