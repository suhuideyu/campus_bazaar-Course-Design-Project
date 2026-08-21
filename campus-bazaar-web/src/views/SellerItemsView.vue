<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { itemApi, userApi } from '../api/index'
import ItemCard from '../components/ItemCard.vue'

const route = useRoute()
const router = useRouter()
const sellerId = Number(route.params.sellerId)

const seller = ref({})
const items = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [userRes, itemsRes] = await Promise.all([
      userApi.getUserById(sellerId),
      itemApi.getBySellerOnSale(sellerId)
    ])
    seller.value = userRes.data
    items.value = itemsRes.data
  } catch { }
  loading.value = false
})
</script>

<template>
  <div class="seller-page container">
    <!-- 返回按钮 -->
    <div class="back-row">
      <button class="back-btn" @click="router.back()">← 返回</button>
    </div>

    <!-- 卖家信息头 -->
    <div class="seller-header" v-if="seller.nickname">
      <div class="seller-avatar">
        <img v-if="seller.avatar" :src="seller.avatar" />
        <div v-else class="avatar-placeholder">{{ seller.nickname[0] }}</div>
      </div>
      <div class="seller-info">
        <h2>{{ seller.nickname }}</h2>
        <span class="seller-school">{{ seller.school || '' }}</span>
        <span class="seller-credit">信用分 {{ seller.creditScore }}</span>
      </div>
    </div>

    <h3 class="section-title">Ta 的在售商品（{{ items.length }}）</h3>

    <!-- 商品网格 -->
    <div v-if="loading" class="grid-loading">
      <el-skeleton :rows="0" animated v-for="i in 4" :key="i" class="skel-card">
        <template #template>
          <el-skeleton-item variant="image" class="skel-img" />
          <div class="skel-body">
            <el-skeleton-item variant="h3" style="width:80%;margin-bottom:8px" />
            <el-skeleton-item variant="text" style="width:50%" />
          </div>
        </template>
      </el-skeleton>
    </div>

    <el-empty v-else-if="items.length === 0" description="Ta 还没有在售商品" :image-size="100" />

    <div v-else class="item-grid">
      <ItemCard v-for="item in items" :key="item.id" :item="item" />
    </div>
  </div>
</template>

<style scoped>
.seller-page { padding: 30px 20px 50px; max-width: 1100px; margin: 0 auto; }
.back-row { margin-bottom: 20px; }
.back-btn {
  background: none; border: 1px solid var(--border); border-radius: 8px;
  padding: 6px 14px; cursor: pointer; font-size: 14px; color: var(--text-muted);
  transition: all 0.15s;
}
.back-btn:hover { border-color: var(--primary); color: var(--primary); }

.seller-header { display: flex; align-items: center; gap: 16px; margin-bottom: 28px; }
.seller-avatar { width: 64px; height: 64px; flex-shrink: 0; }
.seller-avatar img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
.avatar-placeholder {
  width: 64px; height: 64px; border-radius: 50%;
  background: var(--primary); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 24px;
}
.seller-info { display: flex; flex-direction: column; gap: 4px; }
.seller-info h2 { margin: 0; font-size: 22px; }
.seller-school { font-size: 13px; color: var(--text-muted); }
.seller-credit { font-size: 13px; color: var(--primary); font-weight: 600; }
.section-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: var(--text); }

.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 16px;
}
@media (max-width: 480px) {
  .item-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
}

.grid-loading {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 16px;
}
.skel-card { border-radius: 12px; overflow: hidden; background: #fff; box-shadow: var(--shadow); }
.skel-img { width: 100%; aspect-ratio: 4/3; display: block; }
.skel-body { padding: 12px; }
@media (max-width: 480px) {
  .grid-loading { grid-template-columns: repeat(2, 1fr); gap: 10px; }
}
</style>
