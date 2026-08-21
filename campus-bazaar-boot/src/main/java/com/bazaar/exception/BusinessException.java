package com.bazaar.exception;

/**
 * 业务异常（可预期的错误，如商品不存在、无权操作）
 * 技术点：
 * - 继承 RuntimeException，Service 中可以直接 throw，不需要每层都写 throws；
 * - code 保存业务响应码，GlobalExceptionHandler 会把它放进统一 JSON 结果；
 * - 用静态工厂方法 notFound/forbidden/badRequest 可以让抛异常的代码更易读。
 */
public class BusinessException extends RuntimeException {

    /** 对应接口返回的错误码，如 400、403、404 */
    private final int code;

    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }

    public static BusinessException notFound(String resource) {
        return new BusinessException(404, resource + "不存在");
    }

    public static BusinessException forbidden(String action) {
        return new BusinessException(403, "无权" + action);
    }

    public static BusinessException badRequest(String message) {
        return new BusinessException(400, message);
    }

    public int getCode() { return code; }
}
