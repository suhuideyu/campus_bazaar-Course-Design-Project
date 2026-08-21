package com.bazaar.domain;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.math.BigDecimal;
import java.util.Date;

/**
 * 订单实体，对应 cb_order 表
 * 技术点：
 * - 订单对象保存交易快照，例如下单时的价格 price；
 * - 订单状态和商品状态要配合变化，这部分业务规则写在 OrderServiceImpl；
 * - itemTitle/buyerNickname 等是查询订单列表时从关联表补充出来的展示字段。
 */
public class Order {

    private Long id;
    private String orderNo;
    private Long itemId;
    private Long buyerId;
    private Long sellerId;
    private BigDecimal price;
    private String message;
    /**
     * 状态：0=待卖家确认，1=已确认，2=交易完成，3=已取消
     */
    private Integer status;
    private String meetPlace;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date createdAt;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date confirmedAt;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date finishedAt;

    // ===== 关联查询附加字段 =====
    private String itemTitle;
    private String itemImages;
    private String buyerNickname;
    private String buyerSchool;
    private String sellerNickname;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getOrderNo() { return orderNo; }
    public void setOrderNo(String orderNo) { this.orderNo = orderNo; }

    public Long getItemId() { return itemId; }
    public void setItemId(Long itemId) { this.itemId = itemId; }

    public Long getBuyerId() { return buyerId; }
    public void setBuyerId(Long buyerId) { this.buyerId = buyerId; }

    public Long getSellerId() { return sellerId; }
    public void setSellerId(Long sellerId) { this.sellerId = sellerId; }

    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public String getMeetPlace() { return meetPlace; }
    public void setMeetPlace(String meetPlace) { this.meetPlace = meetPlace; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getConfirmedAt() { return confirmedAt; }
    public void setConfirmedAt(Date confirmedAt) { this.confirmedAt = confirmedAt; }

    public Date getFinishedAt() { return finishedAt; }
    public void setFinishedAt(Date finishedAt) { this.finishedAt = finishedAt; }

    public String getItemTitle() { return itemTitle; }
    public void setItemTitle(String itemTitle) { this.itemTitle = itemTitle; }

    public String getItemImages() { return itemImages; }
    public void setItemImages(String itemImages) { this.itemImages = itemImages; }

    public String getBuyerNickname() { return buyerNickname; }
    public void setBuyerNickname(String buyerNickname) { this.buyerNickname = buyerNickname; }

    public String getBuyerSchool() { return buyerSchool; }
    public void setBuyerSchool(String buyerSchool) { this.buyerSchool = buyerSchool; }

    public String getSellerNickname() { return sellerNickname; }
    public void setSellerNickname(String sellerNickname) { this.sellerNickname = sellerNickname; }

    @Override
    public String toString() {
        return "Order{id=" + id + ", orderNo='" + orderNo + "', status=" + status + "}";
    }
}
