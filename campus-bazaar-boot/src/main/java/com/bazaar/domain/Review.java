package com.bazaar.domain;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.util.Date;

public class Review {

    private Long id;
    private Long orderId;
    private Long reviewerId;
    private Long revieweeId;
    private Integer score;
    private String content;
    private String reviewerNickname;
    private String revieweeNickname;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date createdAt;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getOrderId() { return orderId; }
    public void setOrderId(Long orderId) { this.orderId = orderId; }

    public Long getReviewerId() { return reviewerId; }
    public void setReviewerId(Long reviewerId) { this.reviewerId = reviewerId; }

    public Long getRevieweeId() { return revieweeId; }
    public void setRevieweeId(Long revieweeId) { this.revieweeId = revieweeId; }

    public Integer getScore() { return score; }
    public void setScore(Integer score) { this.score = score; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public String getReviewerNickname() { return reviewerNickname; }
    public void setReviewerNickname(String reviewerNickname) { this.reviewerNickname = reviewerNickname; }

    public String getRevieweeNickname() { return revieweeNickname; }
    public void setRevieweeNickname(String revieweeNickname) { this.revieweeNickname = revieweeNickname; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }
}
