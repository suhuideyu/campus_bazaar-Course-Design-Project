package com.bazaar.utils;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * MD5 工具类
 * 技术点：
 * - 工具类的方法通常设计成 static，调用方不需要 new 对象；
 * - MessageDigest 是 JDK 提供的摘要算法 API；
 * - 注意：MD5 仅适合教学演示，真实系统应使用 BCrypt/PBKDF2 等带盐密码算法。
 */
public class MD5Utils {

    /** 私有构造方法：防止外部 new 工具类对象 */
    private MD5Utils() {}

    /**
     * 对字符串进行 MD5 加密
     *
     * @param input 原始字符串
     * @return 32位小写十六进制字符串
     */
    public static String encrypt(String input) {
        try {
            // 获取 MD5 摘要算法实例。
            MessageDigest md = MessageDigest.getInstance("MD5");
            // 把原始字符串按 UTF-8 转成字节，再计算摘要。
            byte[] bytes = md.digest(input.getBytes("UTF-8"));
            StringBuilder sb = new StringBuilder();
            for (byte b : bytes) {
                // 把每个字节转换成两位十六进制字符串。
                sb.append(String.format("%02x", b & 0xff));
            }
            return sb.toString();
        } catch (Exception e) {
            throw new RuntimeException("MD5加密失败", e);
        }
    }

    /**
     * 校验密码
     *
     * @param rawPassword     明文密码
     * @param encodedPassword 加密后的密码
     */
    public static boolean matches(String rawPassword, String encodedPassword) {
        return encrypt(rawPassword).equals(encodedPassword);
    }
}
