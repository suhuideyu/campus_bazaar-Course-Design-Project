package com.bazaar.exception;

import com.bazaar.common.Result;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * 全局异常处理器
 * 所有 Controller 抛出的异常都会被这里统一处理，转为 JSON 返回
 * 技术点：
 * - @RestControllerAdvice 是 Spring MVC 的全局增强，等价于给所有 Controller 做统一异常处理；
 * - @ExceptionHandler 按异常类型匹配处理方法；
 * - 有了全局异常处理，Controller/Service 不需要到处 try-catch。
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /** 处理业务逻辑异常（如：商品不存在、无权操作） */
    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusinessException(BusinessException e) {
        // 业务异常是可预期错误，用 warn 记录即可，不需要打印完整堆栈。
        log.warn("业务异常: [{}] {}", e.getCode(), e.getMessage());
        return Result.fail(e.getCode(), e.getMessage());
    }

    /** 处理参数校验异常 */
    @ExceptionHandler(IllegalArgumentException.class)
    public Result<?> handleIllegalArgument(IllegalArgumentException e) {
        // 参数错误统一返回 400，前端可以据此提示用户修正输入。
        log.warn("参数错误: {}", e.getMessage());
        return Result.badRequest(e.getMessage());
    }

    /** 处理所有未知异常 */
    @ExceptionHandler(Exception.class)
    public Result<?> handleException(Exception e) {
        log.error("系统异常: ", e);
        return Result.fail(500, "服务器内部错误，请稍后再试");
    }
}