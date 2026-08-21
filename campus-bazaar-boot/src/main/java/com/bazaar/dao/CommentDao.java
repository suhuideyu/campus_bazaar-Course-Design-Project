package com.bazaar.dao;

import com.bazaar.domain.Comment;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface CommentDao {

    Comment findById(Long id);

    List<Comment> findByItemId(Long itemId);

    int insert(Comment comment);

    int countByItemId(Long itemId);
}
