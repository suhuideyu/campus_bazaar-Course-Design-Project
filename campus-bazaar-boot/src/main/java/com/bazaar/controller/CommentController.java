package com.bazaar.controller;

import com.bazaar.common.Result;
import com.bazaar.domain.Comment;
import com.bazaar.domain.User;
import com.bazaar.interceptor.LoginInterceptor;
import com.bazaar.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/comments")
public class CommentController {

    @Autowired
    private CommentService commentService;

    /**
     * 获取商品的所有留言
     * GET /api/comments/item/{itemId}
     */
    @GetMapping("/item/{itemId}")
    public Result<List<Comment>> listByItem(@PathVariable Long itemId) {
        return Result.success(commentService.listByItemId(itemId));
    }

    /**
     * 新增留言
     * POST /api/comments
     * Body: {"itemId": 1, "content": "..."}
     */
    @PostMapping
    public Result<Comment> add(@RequestBody Map<String, Object> body, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        Long itemId = Long.valueOf(body.get("itemId").toString());
        String content = (String) body.get("content");
        Comment comment = commentService.addComment(loginUser.getId(), itemId, content);
        return Result.success("留言成功", comment);
    }

    /**
     * 回复留言
     * POST /api/comments/{id}/reply
     * Body: {"content": "..."}
     */
    @PostMapping("/{id}/reply")
    public Result<Comment> reply(@PathVariable Long id, @RequestBody Map<String, String> body, HttpSession session) {
        User loginUser = (User) session.getAttribute(LoginInterceptor.SESSION_USER_KEY);
        String content = body.get("content");
        Comment reply = commentService.addReply(loginUser.getId(), id, content);
        return Result.success("回复成功", reply);
    }
}
