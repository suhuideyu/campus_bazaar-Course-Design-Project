<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { itemApi, categoryApi } from '../api/index'

const router = useRouter()

const form = ref({
  title: '', description: '', images: '',
  price: '', originalPrice: '',
  categoryId: '', conditionLevel: 3
})
const categories = ref([])
const loading = ref(false)
const error = ref('')

const conditionOptions = [
  { value: 1, label: '几乎全新', desc: '使用极少，几乎无痕迹' },
  { value: 2, label: '轻微使用', desc: '有轻微使用痕迹' },
  { value: 3, label: '正常使用', desc: '正常使用痕迹' },
  { value: 4, label: '明显使用', desc: '有明显使用痕迹' },
  { value: 5, label: '大量使用', desc: '大量使用痕迹，功能正常' }
]

async function loadCategories() {
  const res = await categoryApi.getAll()
  categories.value = res.data
}

async function handlePublish() {
  error.value = ''
  const { title, price, categoryId } = form.value
  if (!title.trim()) { error.value = '请填写商品标题'; return }
  if (!price || Number(price) <= 0) { error.value = '请填写有效价格'; return }
  if (!categoryId) { error.value = '请选择商品分类'; return }
  loading.value = true
  try {
    const payload = {
      ...form.value,
      price: Number(form.value.price),
      originalPrice: form.value.originalPrice ? Number(form.value.originalPrice) : null,
      categoryId: Number(form.value.categoryId)
    }
    await itemApi.publish(payload)
    window.$toast?.('发布成功，等待审核')
    router.push('/my/items')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(loadCategories)
</script>

<template>
  <div class="container publish-page">
    <div class="page-header">
      <h2>发布商品</h2>
      <p class="sub">填写商品信息，发布后等待审核即可上架</p>
    </div>

    <div class="publish-body">
      <form @submit.prevent="handlePublish" class="publish-form card">
        <!-- 基本信息 -->
        <div class="section-title">基本信息</div>

        <div class="form-group">
          <label class="form-label">商品标题 <span class="req">*</span></label>
          <input v-model="form.title" class="form-input" placeholder="简洁描述商品，如：高等数学第七版（上下册）" maxlength="50" />
          <span class="form-hint">{{ form.title.length }}/50</span>
        </div>

        <div class="form-row-3">
          <div class="form-group">
            <label class="form-label">分类 <span class="req">*</span></label>
            <select v-model="form.categoryId" class="form-select">
              <option value="">请选择分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">出售价（元）<span class="req">*</span></label>
            <input v-model="form.price" class="form-input" type="number" step="0.01" min="0.01" placeholder="0.00" />
          </div>
          <div class="form-group">
            <label class="form-label">原价（元，选填）</label>
            <input v-model="form.originalPrice" class="form-input" type="number" step="0.01" min="0" placeholder="0.00" />
          </div>
        </div>

        <!-- 成色 -->
        <div class="form-group">
          <label class="form-label">商品成色 <span class="req">*</span></label>
          <div class="condition-grid">
            <label
              v-for="opt in conditionOptions"
              :key="opt.value"
              class="condition-option"
              :class="{ active: form.conditionLevel === opt.value }"
            >
              <input type="radio" :value="opt.value" v-model="form.conditionLevel" class="hidden" />
              <span class="cond-label">{{ opt.label }}</span>
              <span class="cond-desc">{{ opt.desc }}</span>
            </label>
          </div>
        </div>

        <!-- 描述 -->
        <div class="form-group">
          <label class="form-label">商品描述</label>
          <textarea v-model="form.description" class="form-textarea" rows="5" placeholder="详细描述商品情况，如购买时间、使用情况、是否有配件等…" maxlength="1000"></textarea>
          <span class="form-hint">{{ (form.description || '').length }}/1000</span>
        </div>

        <!-- 图片 -->
        <div class="form-group">
          <label class="form-label">商品图片</label>
          <input v-model="form.images" class="form-input" placeholder="图片URL，多张用英文逗号分隔（如：http://...jpg,http://...jpg）" />
          <span class="form-hint">暂不支持上传，请填写图片链接</span>
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <div class="form-actions">
          <button type="button" class="btn btn-ghost btn-lg" @click="$router.back()">取消</button>
          <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
            {{ loading ? '发布中…' : '发布商品' }}
          </button>
        </div>
      </form>

      <!-- 提示卡 -->
      <div class="tip-card card">
        <div class="tip-title">📋 发布须知</div>
        <ul class="tip-list">
          <li>商品须经管理员审核后才会上架</li>
          <li>禁止发布违禁物品、仿冒品</li>
          <li>请如实描述商品成色，保证信用</li>
          <li>建议上传清晰实拍图，提高成交率</li>
          <li>交易完成后买家可对你进行信用评价</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.publish-page { padding: 24px 20px 60px; }
.page-header { margin-bottom: 24px; }
.page-header h2 { font-size: 22px; font-weight: 700; }
.sub { font-size: 14px; color: var(--text-muted); margin-top: 4px; }

.publish-body { display: grid; grid-template-columns: 1fr 280px; gap: 24px; align-items: start; }
@media (max-width: 900px) { .publish-body { grid-template-columns: 1fr; } }

.publish-form { padding: 28px; }
.section-title {
  font-size: 15px; font-weight: 700;
  color: var(--primary);
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--primary-light);
}
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
@media (max-width: 640px) { .form-row-3 { grid-template-columns: 1fr; } }

.condition-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
@media (max-width: 640px) { .condition-grid { grid-template-columns: repeat(2, 1fr); } }
.condition-option {
  border: 2px solid var(--border);
  border-radius: 8px;
  padding: 10px 8px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
  display: flex; flex-direction: column; gap: 3px;
}
.condition-option.active { border-color: var(--primary); background: var(--primary-light); }
.cond-label { font-size: 13px; font-weight: 600; color: var(--text); }
.cond-desc { font-size: 11px; color: var(--text-muted); }
.condition-option.active .cond-label { color: var(--primary); }
.hidden { display: none; }

.error-msg {
  color: var(--danger); font-size: 13px;
  background: #fee2e2; border-radius: 6px;
  padding: 10px 14px; margin-bottom: 16px;
}
.form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 8px; }
.req { color: var(--danger); }

.tip-card { padding: 20px; }
.tip-title { font-size: 14px; font-weight: 700; margin-bottom: 12px; }
.tip-list { padding-left: 18px; display: flex; flex-direction: column; gap: 8px; }
.tip-list li { font-size: 13px; color: var(--text-muted); line-height: 1.6; }
</style>
