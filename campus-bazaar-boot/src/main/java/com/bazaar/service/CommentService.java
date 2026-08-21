package com.bazaar.service;

import com.bazaar.domain.Comment;

import java.util.List;

public interface CommentService {

    List<Comment> listByItemId(Long itemId);

    Comment addComment(Long userId, Long itemId, String content);

    Comment addReply(Long userId, Long commentId, String content);

    Comment getCommentById(Long commentId);
}
