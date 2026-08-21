<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { itemApi, categoryApi } from '../api/index'
import ItemCard from '../components/ItemCard.vue'
import { Icon } from '@iconify/vue'

const route = useRoute()
const router = useRouter()

const categories = ref([])
const items = ref([])
const total = ref(0)
const loading = ref(false)

const query = reactive({
  keyword: route.query.keyword || '',
  categoryId: route.query.categoryId ? Number(route.query.categoryId) : null,
  orderBy: route.query.orderBy || '',
  pageNum: 1,
  pageSize: 12
})

const categoryConfig = {
  '教材课本': { icon: 'ri:book-2-line',        bg: '#eff6ff', color: '#3b82f6' },
  '电子数码': { icon: 'ri:smartphone-line',     bg: '#f5f3ff', color: '#8b5cf6' },
  '生活用品': { icon: 'ri:home-4-line',         bg: '#f0fdf4', color: '#16a34a' },
  '运动装备': { icon: 'ri:football-line',       bg: '#fffbeb', color: '#d97706' },
  '服饰鞋帽': { icon: 'ri:t-shirt-line',        bg: '#fdf2f8', color: '#ec4899' },
  '其他':     { icon: 'ri:apps-line',           bg: '#f9fafb', color: '#6b7280' }
}

const orderOptions = [
  { value: '', label: '综合排序' },
  { value: 'newest', label: '最新发布' },
  { value: 'price_asc', label: '价格最低' },
  { value: 'price_desc', label: '价格最高' }
]

async function loadCategories() {
  const res = await categoryApi.getAll()
  categories.value = res.data
}

async function loadItems() {
  loading.value = true
  try {
    const params = { ...query }
    if (!params.categoryId) delete params.categoryId
    if (!params.keyword) delete params.keyword
    if (!params.orderBy) delete params.orderBy
    const res = await itemApi.getList(params)
    items.value = res.data.list
    total.value = res.data.total
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}

function selectCategory(id) {
  query.categoryId = query.categoryId === id ? null : id
  query.pageNum = 1
  loadItems()
}

function doSearch() {
  query.pageNum = 1
  router.replace({ query: { keyword: query.keyword } })
  loadItems()
}

function clearFilter() {
  query.categoryId = null
  query.keyword = ''
  query.orderBy = ''
  query.pageNum = 1
  loadItems()
}

function onPageChange(p) {
  query.pageNum = p
  window.scrollTo({ top: 0, behavior: 'smooth' })
  loadItems()
}

watch(() => route.query.keyword, (kw) => {
  query.keyword = kw || ''
  query.pageNum = 1
  loadItems()
})

onMounted(() => { loadCategories(); loadItems() })
</script>

<template>
  <div class="home-page">

    <!-- ① Banner -->
    <section class="banner">
      <div class="container banner-inner">
        <div class="banner-text">
          <div class="banner-pill">🔥 本周热卖</div>
          <h1 class="banner-title">校园闲置，轻松出售</h1>
          <p class="banner-desc">发布你的二手物品，让闲置变成零花钱</p>
          <button class="banner-btn" @click="$router.push('/publish')">立即发布 ›</button>
        </div>
        <div class="banner-deco" aria-hidden="true">
          <div class="deco-circle dc1"></div>
          <div class="deco-circle dc2"></div>
          <div class="deco-circle dc3"></div>
        </div>
      </div>
    </section>

    <!-- ② 分类图标区 -->
    <section class="cat-section">
      <div class="container">
        <div class="cat-scroll">
          <!-- 全部 -->
          <div
            class="cat-tile"
            :class="{ active: !query.categoryId }"
            @click="selectCategory(null)"
          >
            <div class="cat-tile-icon" style="background:#f0fdf4">
              <Icon icon="ri:apps-2-line" style="font-size:22px;color:#16a34a" />
            </div>
            <span class="cat-tile-name">全部</span>
          </div>
          <!-- 各分类 -->
          <div
            v-for="cat in categories"
            :key="cat.id"
            class="cat-tile"
            :class="{ active: query.categoryId === cat.id }"
            @click="selectCategory(cat.id)"
          >
            <div
              class="cat-tile-icon"
              :style="{ background: categoryConfig[cat.name]?.bg || '#f3f4f6' }"
            >
              <Icon
                :icon="categoryConfig[cat.name]?.icon || 'ri:price-tag-3-line'"
                :style="{ fontSize: '22px', color: categoryConfig[cat.name]?.color || '#6b7280' }"
              />
            </div>
            <span class="cat-tile-name">{{ cat.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ③ 商品列表区 -->
    <section class="list-section container" id="list-section">

      <!-- 移动端搜索 -->
      <el-input
        v-model="query.keyword"
        class="mobile-search"
        placeholder="搜索二手商品…"
        size="large"
        clearable
        @clear="doSearch"
        @keyup.enter="doSearch"
      >
        <template #suffix>
          <el-icon class="search-icon" @click="doSearch"><Search /></el-icon>
        </template>
      </el-input>

      <!-- 工具栏 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <span class="result-text">
            共 <b>{{ total }}</b> 件商品
          </span>
          <el-tag
            v-if="query.categoryId || query.keyword"
            closable
            type="warning"
            effect="light"
            size="small"
            @close="clearFilter"
            class="filter-chip"
          >
            {{ query.keyword || categories.find(c => c.id === query.categoryId)?.name }}
          </el-tag>
        </div>
        <div class="toolbar-right">
          <el-radio-group v-model="query.orderBy" size="small" @change="val => { query.orderBy=val; query.pageNum=1; loadItems() }">
            <el-radio-button v-for="opt in orderOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </el-radio-button>
          </el-radio-group>
        </div>
      </div>

      <!-- 商品网格 -->
      <div v-if="loading" class="grid-loading">
        <el-skeleton :rows="0" animated v-for="i in 8" :key="i" class="skel-card">
          <template #template>
            <el-skeleton-item variant="image" class="skel-img" />
            <div class="skel-body">
              <el-skeleton-item variant="h3" style="width:80%;margin-bottom:8px" />
              <el-skeleton-item variant="text" style="width:50%" />
            </div>
          </template>
        </el-skeleton>
      </div>

      <el-empty
        v-else-if="items.length === 0"
        description="暂无符合条件的商品"
        :image-size="120"
      >
        <el-button type="primary" @click="clearFilter">清除筛选</el-button>
      </el-empty>

      <div v-else class="item-grid">
        <ItemCard v-for="item in items" :key="item.id" :item="item" />
      </div>

      <!-- 分页 -->
      <div class="pager-wrap">
        <el-pagination
          v-if="total > query.pageSize"
          v-model:current-page="query.pageNum"
          :page-size="query.pageSize"
          :total="total"
          layout="prev, pager, next"
          background
          @current-change="onPageChange"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ====== Banner ====== */
.banner {
  background: linear-gradient(110deg, #ff8c00 0%, #ffa726 60%, #ffca28 100%);
  overflow: hidden;
}
.banner-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 180px;
  padding: 36px 20px 32px;
  position: relative;
}
.banner-text {
  flex: 1;
  z-index: 1;
}
.banner-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(255,255,255,0.22);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 14px;
}
.banner-title {
  font-size: 32px;
  font-weight: 800;
  color: #fff;
  line-height: 1.25;
  margin: 0 0 10px;
  letter-spacing: 0.5px;
}
.banner-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.85);
  margin-bottom: 22px;
  line-height: 1.6;
}
.banner-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 10px 24px;
  background: rgba(255,255,255,0.95);
  color: #ea580c;
  font-size: 14px;
  font-weight: 700;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
  transition: transform 0.15s, box-shadow 0.15s;
  letter-spacing: 0.3px;
}
.banner-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.18);
}

/* 右侧装饰圆 */
.banner-deco { position: absolute; right: 0; top: 0; bottom: 0; width: 340px; pointer-events: none; }
.deco-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
}
.dc1 { width: 260px; height: 260px; right: -80px; top: -60px; }
.dc2 { width: 160px; height: 160px; right: 60px;  top: 20px;  background: rgba(255,255,255,0.10); }
.dc3 { width:  80px; height:  80px; right: 180px; bottom: 20px; background: rgba(255,255,255,0.15); }

@media (max-width: 600px) {
  .banner-title { font-size: 24px; }
  .banner-deco { display: none; }
  .banner-inner { min-height: auto; padding: 28px 16px 24px; }
}


/* ====== 分类图标区 ====== */
.cat-section {
  background: #fff;
  border-bottom: 1px solid var(--border);
  padding: 14px 0 10px;
}
.cat-scroll {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  scrollbar-width: none;
  padding-bottom: 4px;
}
.cat-scroll::-webkit-scrollbar { display: none; }
.cat-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.18s;
  flex-shrink: 0;
  min-width: 60px;
  border: 2px solid transparent;
}
.cat-tile:hover { background: var(--bg); }
.cat-tile.active { border-color: var(--primary); background: var(--primary-light); }
.cat-tile.active .cat-tile-name { color: var(--primary); font-weight: 700; }
.cat-tile-icon {
  width: 46px; height: 46px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  transition: transform 0.18s;
}
.cat-tile:hover .cat-tile-icon { transform: scale(1.12); }
.cat-tile-name { font-size: 12px; color: var(--text-muted); }

/* ====== 列表区 ====== */
.list-section { padding-top: 18px; padding-bottom: 50px; }

.mobile-search { display: none; margin-bottom: 14px; }
@media (max-width: 600px) { .mobile-search { display: flex; } }
.search-icon { cursor: pointer; color: var(--primary); }

/* 工具栏 */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  background: #fff;
  border-radius: 10px;
  padding: 10px 16px;
  margin-bottom: 18px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}
.toolbar-left { display: flex; align-items: center; gap: 8px; }
.result-text { font-size: 13px; color: var(--text-muted); }
.result-text b { color: var(--text); font-weight: 700; }
.filter-chip { cursor: default; }

/* 骨架屏网格 */
.grid-loading {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 16px;
}
.skel-card { border-radius: 12px; overflow: hidden; background: #fff; box-shadow: var(--shadow); }
.skel-img { width: 100%; aspect-ratio: 4/3; display: block; }
.skel-body { padding: 12px; }

/* 商品网格 */
.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 16px;
}
@media (max-width: 480px) {
  .item-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .grid-loading { grid-template-columns: repeat(2, 1fr); gap: 10px; }
}

/* 分页 */
.pager-wrap { display: flex; justify-content: center; padding: 30px 0 0; }

/* Element Plus 样式覆盖 */
:deep(.el-radio-button__inner) { font-size: 13px; }
:deep(.el-pagination.is-background .el-pager li.is-active) {
  background: var(--primary);
}
:deep(.el-pagination.is-background .el-pager li:hover) {
  color: var(--primary);
}
</style>
