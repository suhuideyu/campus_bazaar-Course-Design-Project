package com.bazaar.service;

import com.bazaar.domain.Item;
import com.bazaar.domain.User;
import com.bazaar.vo.PageResult;

public interface AdminService {

    PageResult<User> listUsers(int page, int size);

    void updateUserStatus(Long userId, Integer status);

    PageResult<Item> listItems(int page, int size, Integer status, String keyword);

    void updateItemStatus(Long itemId, Integer status);
}
