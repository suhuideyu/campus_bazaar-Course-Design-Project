<script setup>
defineProps({
  item: { type: Object, required: true }
})

const conditionMap = ['', '几乎全新', '轻微使用', '正常使用', '明显使用', '大量使用']
const statusMap = { 0: { text: '待审核', cls: 'badge-orange' }, 1: { text: '在售', cls: 'badge-green' }, 2: { text: '锁定', cls: 'badge-red' }, 3: { text: '已售', cls: 'badge-gray' }, 4: { text: '下架', cls: 'badge-gray' } }

function firstImage(images) {
  if (!images) return null
  return images.split(',')[0]
}
</script>

<template>
  <router-link :to="`/item/${item.id}`" class="item-card card">
    <div class="item-img-wrap">
      <img v-if="firstImage(item.images)" :src="firstImage(item.images)" :alt="item.title" class="item-img" />
      <div v-else class="item-img-placeholder">📦</div>
      <span class="badge status-badge" :class="statusMap[item.status]?.cls">
        {{ statusMap[item.status]?.text }}
      </span>
    </div>
    <div class="item-body">
      <div class="item-title">{{ item.title }}</div>
      <div class="item-meta">
        <span class="condition">{{ conditionMap[item.conditionLevel] }}</span>
        <span v-if="item.categoryName" class="category-name">{{ item.categoryName }}</span>
      </div>
      <div class="item-footer">
        <div class="price-wrap">
          <span class="price">¥{{ item.price }}</span>
          <span v-if="item.originalPrice" class="original-price">¥{{ item.originalPrice }}</span>
        </div>
        <div class="item-stats">
          <span title="浏览">👁 {{ item.viewCount }}</span>
          <span title="收藏">❤️ {{ item.favCount }}</span>
        </div>
      </div>
      <div v-if="item.sellerNickname" class="seller-info">
        <span class="seller-avatar-text">{{ item.sellerNickname[0] }}</span>
        {{ item.sellerNickname }}
      </div>
    </div>
  </router-link>
</template>

<style scoped>
.item-card {
  display: block;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}
.item-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.item-img-wrap {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
  background: #f3f4f6;
}
.item-img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.item-card:hover .item-img { transform: scale(1.05); }
.item-img-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 48px; color: #d1d5db;
}
.status-badge {
  position: absolute; top: 8px; left: 8px;
  font-size: 11px;
}
.item-body { padding: 12px 14px 14px; }
.item-title {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-bottom: 6px;
  color: var(--text);
}
.item-meta {
  display: flex;
  gap: 6px;
  margin-bottom: 8px;
}
.condition {
  font-size: 11px;
  padding: 2px 6px;
  background: #f0fdf4;
  color: var(--primary);
  border-radius: 4px;
}
.category-name {
  font-size: 11px;
  padding: 2px 6px;
  background: #f3f4f6;
  color: var(--text-muted);
  border-radius: 4px;
}
.item-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.price-wrap { display: flex; align-items: baseline; gap: 6px; }
.price { font-size: 17px; font-weight: 700; color: #dc2626; }
.original-price { font-size: 12px; color: var(--text-muted); text-decoration: line-through; }
.item-stats { display: flex; gap: 8px; font-size: 12px; color: var(--text-muted); }
.seller-info {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--border);
}
.seller-avatar-text {
  width: 18px; height: 18px;
  border-radius: 50%;
  background: var(--primary-light);
  color: var(--primary);
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 700;
}
</style>
