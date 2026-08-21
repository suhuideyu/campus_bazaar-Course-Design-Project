<script setup>
import { ref, onMounted } from 'vue'
import { userApi, itemApi } from '../api/index'

const favorites = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const res = await userApi.getMyFavorites()
    favorites.value = res.data
  } catch (e) {
    window.$toast?.(e.message, 'error')
  } finally {
    loading.value = false
  }
}

async function removeFav(fav) {
  try {
    await itemApi.removeFavorite(fav.itemId)
    favorites.value = favorites.value.filter(f => f.id !== fav.id)
    window.$toast?.('已取消收藏')
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
      <h2>我的收藏</h2>
    </div>

    <div v-if="loading" class="loading-wrap">加载中…</div>
    <div v-else-if="favorites.length === 0" class="empty-state">
      <div class="empty-icon">❤️</div>
      <p>还没有收藏商品</p>
      <router-link to="/" class="btn btn-outline">去逛逛</router-link>
    </div>
    <div v-else class="fav-list">
      <div v-for="fav in favorites" :key="fav.id" class="fav-row card">
        <router-link :to="`/item/${fav.itemId}`" class="fav-img-wrap">
          <img v-if="fav.itemImages" :src="fav.itemImages.split(',')[0]" class="fav-img" />
          <div v-else class="fav-img-placeholder">📦</div>
        </router-link>
        <div class="fav-info">
          <router-link :to="`/item/${fav.itemId}`" class="fav-title">
            {{ fav.itemTitle || `商品 #${fav.itemId}` }}
          </router-link>
          <div class="fav-price" v-if="fav.itemPrice">¥{{ fav.itemPrice }}</div>
          <div class="fav-date">收藏于 {{ fav.createdAt }}</div>
        </div>
        <button class="btn btn-ghost btn-sm" @click="removeFav(fav)">取消收藏</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sub-page { padding: 24px 20px 60px; }
.sub-header { margin-bottom: 20px; }
.back-link { font-size: 13px; color: var(--primary); display: block; margin-bottom: 8px; }
.sub-header h2 { font-size: 20px; font-weight: 700; }

.fav-list { display: flex; flex-direction: column; gap: 12px; }
.fav-row { display: flex; align-items: center; gap: 14px; padding: 14px; }
.fav-img-wrap { flex-shrink: 0; }
.fav-img { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; }
.fav-img-placeholder {
  width: 80px; height: 80px; border-radius: 8px;
  background: #f3f4f6; display: flex; align-items: center;
  justify-content: center; font-size: 28px; color: #d1d5db;
}
.fav-info { flex: 1; display: flex; flex-direction: column; gap: 5px; }
.fav-title { font-size: 15px; font-weight: 600; color: var(--text); text-decoration: none; }
.fav-title:hover { color: var(--primary); }
.fav-price { font-size: 16px; font-weight: 700; color: #dc2626; }
.fav-date { font-size: 12px; color: var(--text-muted); }
</style>
