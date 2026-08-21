<script setup>
import { ref, onMounted } from 'vue'
import { orderApi } from '../api/index'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const tab = ref('buy')
const buyOrders = ref([])
const sellOrders = ref([])
const loading = ref(true)

const orderStatusMap = {
  0: { text: '待确认', type: 'warning' },
  1: { text: '已确认', type: 'primary' },
  2: { text: '已完成', type: 'success' },
  3: { text: '已取消', type: 'info' }
}

async function load() {
  loading.value = true
  try {
    const [buyRes, sellRes] = await Promise.all([
      orderApi.getMyBuyOrders(),
      orderApi.getMySellOrders()
    ])
    buyOrders.value = buyRes.data
    sellOrders.value = sellRes.data
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}

async function doAction(action, orderId) {
  try {
    await action(orderId)
    ElMessage.success('操作成功')
    await load()
  } catch (e) {
    ElMessage.error(e.message)
  }
}

const currentOrders = () => tab.value === 'buy' ? buyOrders.value : sellOrders.value

onMounted(load)
</script>

<template>
  <div class="container sub-page">
    <div class="sub-header">
      <router-link to="/my" class="back-link">
        <el-icon><ArrowLeft /></el-icon> 我的主页
      </router-link>
      <h2>我的订单</h2>
    </div>

    <el-tabs v-model="tab" class="order-tabs">
      <el-tab-pane :label="`我买到的 (${buyOrders.length})`" name="buy" />
      <el-tab-pane :label="`我卖出的 (${sellOrders.length})`" name="sell" />
    </el-tabs>

    <div v-if="loading" v-loading="true" class="loading-placeholder"></div>

    <el-empty v-else-if="currentOrders().length === 0"
      :description="tab === 'buy' ? '还没有购买记录' : '还没有卖出记录'"
      :image-size="120"
    />

    <div v-else class="order-list">
      <el-card
        v-for="order in currentOrders()"
        :key="order.id"
        class="order-card"
        shadow="hover"
      >
        <!-- 卡片头 -->
        <template #header>
          <div class="order-head">
            <span class="order-no">{{ order.orderNo }}</span>
            <el-tag :type="orderStatusMap[order.status]?.type" size="small">
              {{ orderStatusMap[order.status]?.text }}
            </el-tag>
          </div>
        </template>

        <!-- 卡片体 -->
        <div class="order-body">
          <div class="order-img">
            <img v-if="order.itemImages" :src="order.itemImages.split(',')[0]" />
            <el-icon v-else size="28" color="#d1d5db"><Box /></el-icon>
          </div>
          <div class="order-info">
            <router-link :to="`/item/${order.itemId}`" class="order-title">
              {{ order.itemTitle || `商品 #${order.itemId}` }}
            </router-link>
            <div class="order-meta">
              <span v-if="tab==='buy'">卖家：{{ order.sellerNickname }}</span>
              <span v-else>买家：{{ order.buyerNickname }}</span>
              <el-text type="danger" style="font-weight:700">¥{{ order.price }}</el-text>
            </div>
            <div v-if="order.meetPlace" class="order-detail-line">
              <el-icon><Location /></el-icon> {{ order.meetPlace }}
            </div>
            <div v-if="order.message" class="order-detail-line">
              <el-icon><ChatDotRound /></el-icon> {{ order.message }}
            </div>
            <div class="order-time">{{ order.createdAt }}</div>
          </div>
        </div>

        <!-- 操作 -->
        <div class="order-actions">
          <template v-if="tab === 'buy'">
            <el-button
              v-if="order.status === 1"
              type="primary" size="small" round
              @click="doAction(orderApi.finish, order.id)"
            >确认完成</el-button>
            <el-button
              v-if="order.status < 2"
              size="small" round
              @click="doAction(orderApi.cancel, order.id)"
            >取消订单</el-button>
          </template>
          <template v-else>
            <el-button
              v-if="order.status === 0"
              type="primary" size="small" round
              @click="doAction(orderApi.confirm, order.id)"
            >确认接单</el-button>
            <el-button
              v-if="order.status < 2"
              size="small" round
              @click="doAction(orderApi.cancel, order.id)"
            >拒绝/取消</el-button>
          </template>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { orderApi } from '../api/index'
export default { setup() { return { orderApi } } }
</script>

<style scoped>
.sub-page { padding: 24px 20px 60px; }
.sub-header { margin-bottom: 16px; }
.back-link { display: inline-flex; align-items: center; gap: 4px; font-size: 13px; color: var(--primary); margin-bottom: 8px; }
.sub-header h2 { font-size: 20px; font-weight: 700; }
.order-tabs { margin-bottom: 16px; }
.loading-placeholder { height: 200px; }
.order-list { display: flex; flex-direction: column; gap: 14px; }
.order-card { border-radius: 12px; }
.order-head { display: flex; align-items: center; justify-content: space-between; }
.order-no { font-size: 12px; color: var(--text-muted); font-family: monospace; }
.order-body { display: flex; gap: 14px; }
.order-img {
  flex-shrink: 0; width: 72px; height: 72px;
  border-radius: 8px; overflow: hidden;
  background: #f3f4f6;
  display: flex; align-items: center; justify-content: center;
}
.order-img img { width: 100%; height: 100%; object-fit: cover; }
.order-info { flex: 1; display: flex; flex-direction: column; gap: 5px; }
.order-title { font-size: 14px; font-weight: 600; color: var(--text); text-decoration: none; }
.order-title:hover { color: var(--primary); }
.order-meta { display: flex; gap: 14px; align-items: center; font-size: 13px; color: var(--text-muted); }
.order-detail-line { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--text-muted); }
.order-time { font-size: 12px; color: #9ca3af; }
.order-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); }
</style>
