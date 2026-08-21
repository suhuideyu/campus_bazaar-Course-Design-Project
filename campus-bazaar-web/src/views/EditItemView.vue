<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { itemApi, categoryApi } from '../api/index'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const form = ref(null)
const categories = ref([])
const loading = ref(false)
const fetchLoading = ref(true)
const error = ref('')

const conditionOptions = [
  { value: 1, label: '几乎全新' }, { value: 2, label: '轻微使用' },
  { value: 3, label: '正常使用' }, { value: 4, label: '明显使用' },
  { value: 5, label: '大量使用' }
]

async function load() {
  fetchLoading.value = true
  try {
    const [itemRes, catRes] = await Promise.all([
      itemApi.getDetail(route.params.id),
      categoryApi.getAll()
    ])
    const item = itemRes.data
    if (item.sellerId !== userStore.user?.id) {
      window.$toast?.('无权编辑此商品', 'error')
      router.push('/')
      return
    }
    form.value = {
      title: item.title,
      description: item.description || '',
      images: item.images || '',
      price: item.price,
      originalPrice: item.originalPrice || '',
      categoryId: item.categoryId,
      conditionLevel: item.conditionLevel
    }
    categories.value = catRes.data
  } catch (e) {
    window.$toast?.(e.message, 'error')
    router.push('/my/items')
  } finally {
    fetchLoading.value = false
  }
}

async function handleSave() {
  error.value = ''
  if (!form.value.title.trim()) { error.value = '请填写商品标题'; return }
  if (!form.value.price || Number(form.value.price) <= 0) { error.value = '请填写有效价格'; return }
  loading.value = true
  try {
    await itemApi.update(route.params.id, {
      ...form.value,
      price: Number(form.value.price),
      originalPrice: form.value.originalPrice ? Number(form.value.originalPrice) : null,
      categoryId: Number(form.value.categoryId)
    })
    window.$toast?.('商品信息已更新')
    router.push('/my/items')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="container sub-page">
    <div class="sub-header">
      <router-link to="/my/items" class="back-link">← 我发布的</router-link>
      <h2>编辑商品</h2>
    </div>

    <div v-if="fetchLoading" class="loading-wrap">加载中…</div>
    <form v-else-if="form" @submit.prevent="handleSave" class="edit-form card">
      <div class="form-group">
        <label class="form-label">商品标题</label>
        <input v-model="form.title" class="form-input" maxlength="50" />
      </div>
      <div class="form-row-3">
        <div class="form-group">
          <label class="form-label">分类</label>
          <select v-model="form.categoryId" class="form-select">
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">出售价（元）</label>
          <input v-model="form.price" class="form-input" type="number" step="0.01" min="0.01" />
        </div>
        <div class="form-group">
          <label class="form-label">原价（元，选填）</label>
          <input v-model="form.originalPrice" class="form-input" type="number" step="0.01" />
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">成色</label>
        <div class="cond-row">
          <label
            v-for="opt in conditionOptions" :key="opt.value"
            class="cond-opt"
            :class="{ active: form.conditionLevel === opt.value }"
          >
            <input type="radio" :value="opt.value" v-model="form.conditionLevel" class="hidden" />
            {{ opt.label }}
          </label>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">商品描述</label>
        <textarea v-model="form.description" class="form-textarea" rows="5" maxlength="1000"></textarea>
      </div>
      <div class="form-group">
        <label class="form-label">图片链接</label>
        <input v-model="form.images" class="form-input" placeholder="多张用英文逗号分隔" />
      </div>
      <div v-if="error" class="error-msg">{{ error }}</div>
      <div class="form-actions">
        <button type="button" class="btn btn-ghost btn-lg" @click="$router.back()">取消</button>
        <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
          {{ loading ? '保存中…' : '保存修改' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.sub-page { padding: 24px 20px 60px; }
.sub-header { margin-bottom: 20px; }
.back-link { font-size: 13px; color: var(--primary); display: block; margin-bottom: 8px; }
.sub-header h2 { font-size: 20px; font-weight: 700; }
.edit-form { padding: 28px; max-width: 760px; }
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
@media (max-width: 640px) { .form-row-3 { grid-template-columns: 1fr; } }
.cond-row { display: flex; gap: 8px; flex-wrap: wrap; }
.cond-opt {
  padding: 6px 14px; border-radius: 6px;
  border: 2px solid var(--border); cursor: pointer;
  font-size: 13px; transition: all 0.2s;
}
.cond-opt.active { border-color: var(--primary); background: var(--primary-light); color: var(--primary); font-weight: 600; }
.hidden { display: none; }
.error-msg {
  color: var(--danger); font-size: 13px;
  background: #fee2e2; border-radius: 6px;
  padding: 10px 14px; margin-bottom: 16px;
}
.form-actions { display: flex; gap: 12px; justify-content: flex-end; }
</style>
