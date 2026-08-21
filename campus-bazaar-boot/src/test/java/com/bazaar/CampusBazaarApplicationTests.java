package com.bazaar;

import com.bazaar.domain.Item;
import com.bazaar.domain.Order;
import com.bazaar.domain.User;
import com.bazaar.service.ItemService;
import com.bazaar.service.OrderService;
import com.bazaar.service.UserService;
import com.bazaar.vo.ItemQueryVO;
import com.bazaar.vo.PageResult;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;

/**
 * SpringBoot 集成测试
 * @SpringBootTest 会启动完整的 Spring 应用上下文
 */
@SpringBootTest
public class CampusBazaarApplicationTests {

    @Autowired
    private UserService userService;

    @Autowired
    private ItemService itemService;

    @Autowired
    private OrderService orderService;

    @Test
    public void contextLoads() {
        // 验证 Spring 上下文正常启动
        assertNotNull(userService);
        assertNotNull(itemService);
        assertNotNull(orderService);
        System.out.println("✅ Spring 上下文加载成功");
    }

    @Test
    public void testUserRegisterAndLogin() {
        User user = new User();
        user.setUsername("boot_test_" + System.currentTimeMillis());
        user.setPassword("123456");
        user.setNickname("Boot测试用户");
        user.setSchool("信阳学院");

        userService.register(user);
        assertNotNull(user.getId());
        System.out.println("✅ 注册成功，ID=" + user.getId());

        User logged = userService.login(user.getUsername(), "123456");
        assertEquals(user.getUsername(), logged.getUsername());
        System.out.println("✅ 登录成功：" + logged.getNickname());
    }

    @Test
    public void testItemList() {
        ItemQueryVO query = new ItemQueryVO();
        query.setPageNum(1);
        query.setPageSize(5);

        PageResult<Item> result = itemService.getItemList(query);
        System.out.println("✅ 商品列表，总数=" + result.getTotal());
        result.getList().forEach(i ->
                System.out.printf("  [%d] %s ¥%.2f (%s)%n",
                        i.getId(), i.getTitle(), i.getPrice(), i.getCategoryName())
        );
        assertTrue(result.getTotal() >= 0);
    }

    @Test
    public void testPublishItem() {
        Item item = new Item();
        item.setSellerId(2L);
        item.setCategoryId(1);
        item.setTitle("SpringBoot实战（第2版）");
        item.setDescription("9成新，只看了前5章");
        item.setPrice(new BigDecimal("28.00"));
        item.setConditionLevel(2);

        itemService.publishItem(item);
        assertNotNull(item.getId());
        System.out.println("✅ 发布成功，ID=" + item.getId());
    }

    @Test
    public void testFullOrderFlow() {
        System.out.println("=== 完整交易流程测试 ===");

        // 1. 找一个在售商品
        ItemQueryVO q = new ItemQueryVO();
        q.setPageSize(1);
        PageResult<Item> result = itemService.getItemList(q);
        if (result.getList().isEmpty()) {
            System.out.println("无在售商品，跳过测试");
            return;
        }
        Item item = result.getList().get(0);
        Long sellerId = item.getSellerId();
        // 买家不能是卖家本人，选一个不同的用户
        Long buyerId = sellerId.equals(3L) ? 2L : 3L;

        System.out.println("1. 购买商品：" + item.getTitle());
        Order order = orderService.submitOrder(item.getId(), buyerId, "测试订单", "测试地点");
        assertNotNull(order.getId());
        System.out.println("   订单号：" + order.getOrderNo());

        System.out.println("2. 卖家确认订单");
        orderService.confirmOrder(order.getId(), sellerId);

        System.out.println("3. 买家完成交易");
        orderService.finishOrder(order.getId(), buyerId);

        System.out.println("✅ 完整流程测试通过！");
    }
}