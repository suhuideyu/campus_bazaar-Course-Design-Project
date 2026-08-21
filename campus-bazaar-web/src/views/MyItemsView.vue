<script setup>
import { ref, onMounted } from 'vue'
import { itemApi } from '../api/index'
import { useUserStore } from '../stores/user'
import ItemCard from '../components/ItemCard.vue'

const userStore = useUserStore()
const items = ref([])
const loading = ref(true)

const statusMap = { 0:'待审核', 1:'在售', 2:'锁定中', 3:'已售出', 4:'已下架' }

async function load() {
  loading.value = true
  try {
    const res = await itemApi.getBySeller(userStore.user.id)
    items.value = res.data
  } catch (e) {
    window.$toast?.(e.message, 'error')
  } finally {
    loading.value = false
  }
}

async function takeDown(item) {
  if (!confirm(`确认下架「${item.title}」？`)) return
  try {
    await itemApi.takeDown(item.id)
    item.status = 4
    window.$toast?.('已下架')
  } catch (e) {
    window.$toast?.(e.message, 'error')
  }
}

onMounted(load)
</script>

<template>
  <div class="container sub-page">
    <div class="sub-header">
      <router-link to="/my" class="back-link">← 我的主页</router-link>
      <h2>我发布的商品</h2>
    </div>

    <div v-if="loading" class="loading-wrap">加载中…</div>
    <div v-else-if="items.length === 0" class="empty-state">
      <div class="empty-icon">📦</div>
      <p>还没有发布过商品</p>
      <router-link to="/publish" class="btn btn-primary">去发布</router-link>
    </div>
    <div v-else class="item-list">
      <div v-for="item in items" :key="item.id" class="item-row card">
        <router-link :to="`/item/${item.id}`" class="item-row-img-wrap">
          <img v-if="item.images" :src="item.images.split(',')[0]" class="item-row-img" />
          <div v-else class="item-row-img-placeholder">📦</div>
        </router-link>
        <div class="item-row-info">
          <router-link :to="`/item/${item.id}`" class="item-row-title">{{ item.title }}</router-link>
          <div class="item-row-meta">
            <span class="badge" :class="item.status===1?'badge-green':item.status===4?'badge-red':'badge-yellow'">
              {{ statusMap[item.status] }}
            </span>
            <span class="row-price">¥{{ item.price }}</span>
            <span class="row-stat">👁 {{ item.viewCount }} · ❤️ {{ item.favCount }}</span>
          </div>
          <div class="row-date">{{ item.createdAt }}</div>
        </div>
        <div class="item-row-actions">
          <router-link :to="`/edit/${item.id}`" class="btn btn-outline btn-sm">编辑</router-link>
          <button v-if="item.status !== 4 && item.status !== 3" class="btn btn-ghost btn-sm" @click="takeDown(item)">下架</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sub-page { padding: 24px 20px 60px; }
.sub-header { margin-bottom: 20px; }
.back-link { font-size: 13px; color: var(--primary); display: block; margin-bottom: 8px; }
.sub-header h2 { font-size: 20px; font-weight: 700; }

.item-list { display: flex; flex-direction: column; gap: 12px; }
.item-row {
  display: flex; align-items: center; gap: 16px;
  padding: 14px;
}
.item-row-img-wrap { flex-shrink: 0; }
.item-row-img { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; }
.item-row-img-placeholder {
  width: 80px; height: 80px; border-radius: 8px;
  background: #f3f4f6; display: flex; align-items: center;
  justify-content: center; font-size: 28px; color: #d1d5db;
}
.item-row-info { flex: 1; display: flex; flex-direction: column; gap: 6px; }
.item-row-title { font-size: 15px; font-weight: 600; color: var(--text); text-decoration: none; }
.item-row-title:hover { color: var(--primary); }
.item-row-meta { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.row-price { font-size: 15px; font-weight: 700; color: #dc2626; }
.row-stat { font-size: 12px; color: var(--text-muted); }
.row-date { font-size: 12px; color: var(--text-muted); }
.item-row-actions { display: flex; gap: 8px; flex-shrink: 0; }
</style>
