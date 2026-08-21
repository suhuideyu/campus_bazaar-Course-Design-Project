package com.bazaar.service.impl;

import com.bazaar.dao.CommentDao;
import com.bazaar.domain.Comment;
import com.bazaar.exception.BusinessException;
import com.bazaar.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class CommentServiceImpl implements CommentService {

    @Autowired
    private CommentDao commentDao;

    @Override
    public List<Comment> listByItemId(Long itemId) {
        List<Comment> all = commentDao.findByItemId(itemId);
        Map<Long, Comment> map = new HashMap<>();
        List<Comment> roots = new ArrayList<>();

        for (Comment c : all) {
            if (c.getReplyId() == null) {
                roots.add(c);
            }
            map.put(c.getId(), c);
        }

        for (Comment c : all) {
            if (c.getReplyId() != null) {
                Comment parent = map.get(c.getReplyId());
                if (parent != null) {
                    if (parent.getReplies() == null) {
                        parent.setReplies(new ArrayList<>());
                    }
                    parent.getReplies().add(c);
                }
            }
        }

        return roots;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Comment addComment(Long userId, Long itemId, String content) {
        if (content == null || content.trim().isEmpty()) {
            throw new IllegalArgumentException("留言内容不能为空");
        }
        if (content.length() > 200) {
            throw new IllegalArgumentException("留言内容不能超过200字");
        }
        Comment c = new Comment();
        c.setUserId(userId);
        c.setItemId(itemId);
        c.setContent(content.trim());
        commentDao.insert(c);
        return c;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Comment addReply(Long userId, Long commentId, String content) {
        if (content == null || content.trim().isEmpty()) {
            throw new IllegalArgumentException("回复内容不能为空");
        }
        if (content.length() > 200) {
            throw new IllegalArgumentException("回复内容不能超过200字");
        }
        Comment parent = getCommentById(commentId);
        Comment reply = new Comment();
        reply.setUserId(userId);
        reply.setItemId(parent.getItemId());
        reply.setContent(content.trim());
        reply.setReplyId(commentId);
        commentDao.insert(reply);
        return reply;
    }

    @Override
    public Comment getCommentById(Long commentId) {
        Comment c = commentDao.findById(commentId);
        if (c == null) {
            throw BusinessException.notFound("留言");
        }
        return c;
    }
}
