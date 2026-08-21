package com.bazaar.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Date;

/**
 * 用户实体，对应 cb_user 表
 * 技术点：
 * - 实体类也叫 JavaBean/POJO，字段对应数据库表列；
 * - Spring MVC 接收 JSON 请求体时，会通过 setter 把 JSON 字段填入对象；
 * - Controller 返回对象时，Jackson 会通过 getter 把对象转换成 JSON；
 * - MyBatis 根据 mapper XML 的 resultMap，把查询结果封装成 User 对象。
 */
public class User {

    /** 主键 ID，数据库自增 */
    private Long id;
    /** 登录账号，要求唯一 */
    private String username;

    @JsonProperty("password")
    private String password;

    private String nickname;
    private String avatar;
    private String phone;
    private String school;
    private Integer creditScore;
    /** 角色：0=普通用户，1=管理员 */
    private Integer role;
    /** 状态：0=禁用，1=正常 */
    private Integer status;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai") // 技术点：控制 Date 转 JSON 的格式
    private Date createdAt;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "Asia/Shanghai")
    private Date updatedAt;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getNickname() { return nickname; }
    public void setNickname(String nickname) { this.nickname = nickname; }

    public String getAvatar() { return avatar; }
    public void setAvatar(String avatar) { this.avatar = avatar; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getSchool() { return school; }
    public void setSchool(String school) { this.school = school; }

    public Integer getCreditScore() { return creditScore; }
    public void setCreditScore(Integer creditScore) { this.creditScore = creditScore; }

    public Integer getRole() { return role; }
    public void setRole(Integer role) { this.role = role; }

    public Integer getStatus() { return status; }
    public void setStatus(Integer status) { this.status = status; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }

    public Date getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Date updatedAt) { this.updatedAt = updatedAt; }

    @Override
    public String toString() {
        return "User{id=" + id + ", username='" + username + "', nickname='" + nickname + "'}";
    }
}
