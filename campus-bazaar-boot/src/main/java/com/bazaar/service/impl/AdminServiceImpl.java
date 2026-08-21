package com.bazaar.service.impl;

import com.bazaar.dao.ItemDao;
import com.bazaar.dao.UserDao;
import com.bazaar.domain.Item;
import com.bazaar.domain.User;
import com.bazaar.exception.BusinessException;
import com.bazaar.service.AdminService;
import com.bazaar.vo.ItemQueryVO;
import com.bazaar.vo.PageResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class AdminServiceImpl implements AdminService {

    @Autowired
    private UserDao userDao;

    @Autowired
    private ItemDao itemDao;

    @Override
    public PageResult<User> listUsers(int page, int size) {
        int offset = (page - 1) * size;
        List<User> list = userDao.findAll(offset, size);
        long total = userDao.countAll();
        // 不返回密码
        for (User u : list) {
            u.setPassword(null);
        }
        return new PageResult<>(total, list);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateUserStatus(Long userId, Integer status) {
        User user = userDao.findById(userId);
        if (user == null) {
            throw BusinessException.notFound("用户");
        }
        if (status != 0 && status != 1) {
            throw new IllegalArgumentException("状态值无效，只能为0（禁用）或1（正常）");
        }
        userDao.updateStatus(userId, status);
    }

    @Override
    public PageResult<Item> listItems(int page, int size, Integer status, String keyword) {
        ItemQueryVO query = new ItemQueryVO();
        query.setPageNum(page);
        query.setPageSize(size);
        query.setStatus(status);
        query.setKeyword(keyword);
        query.setAdminMode(true);

        List<Item> list = itemDao.findByCondition(query);
        long total = itemDao.countByCondition(query);
        return new PageResult<>(total, list);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void updateItemStatus(Long itemId, Integer status) {
        Item item = itemDao.findById(itemId);
        if (item == null) {
            throw BusinessException.notFound("商品");
        }
        if (status < 0 || status > 4) {
            throw new IllegalArgumentException("商品状态无效（0-4）");
        }
        itemDao.updateStatus(itemId, status);
    }
}
