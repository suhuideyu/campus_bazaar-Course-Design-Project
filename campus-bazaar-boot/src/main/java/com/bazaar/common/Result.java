package com.bazaar.common;

/**
 * 统一API响应结构
 * 使用泛型支持任意类型的data
 */
public class Result<T> {

    private int code;
    private String message;
    private T data;

    // 私有构造（通过静态工厂方法创建）
    private Result(int code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    /** 成功，带数据 */
    public static <T> Result<T> success(T data) {
        return new Result<>(200, "操作成功", data);
    }

    /** 成功，带自定义消息 */
    public static <T> Result<T> success(String message, T data) {
        return new Result<>(200, message, data);
    }

    /** 成功，无数据 */
    public static <T> Result<T> success() {
        return new Result<>(200, "操作成功", null);
    }

    /** 失败 */
    public static <T> Result<T> fail(int code, String message) {
        return new Result<>(code, message, null);
    }

    /** 参数错误（400） */
    public static <T> Result<T> badRequest(String message) {
        return new Result<>(400, message, null);
    }

    /** 未登录（401） */
    public static <T> Result<T> unauthorized() {
        return new Result<>(401, "请先登录", null);
    }

    /** 无权限（403） */
    public static <T> Result<T> forbidden() {
        return new Result<>(403, "无权限执行此操作", null);
    }
    /** 404 资源不存在 */
    public static <T> Result<T> notFound(String message) {
        return new Result<>(404, message, null);
    }

    // ===================== 以下是补全的 getter & setter =====================
    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }
}
