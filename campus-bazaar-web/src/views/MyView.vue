<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../api/index'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const user = ref(null)
const editing = ref(false)
const loading = ref(false)
const form = ref({})

function startEdit() {
  form.value = {
    nickname: user.value.nickname,
    phone: user.value.phone || '',
    school: user.value.school || '',
    avatar: user.value.avatar || ''
  }
  editing.value = true
}

async function saveEdit() {
  loading.value = true
  try {
    await userApi.updateMe(form.value)
    await userStore.fetchMe()
    user.value = userStore.user
    editing.value = false
    window.$toast?.('个人信息已更新')
  } catch (e) {
    window.$toast?.(e.message, 'error')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await userStore.fetchMe()
  user.value = userStore.user
})
</script>

<template>
  <div class="container my-page">
    <div v-if="!user" class="loading-wrap">加载中…</div>
    <template v-else>
      <div class="my-header card">
        <div class="avatar-large">
          <img v-if="user.avatar" :src="user.avatar" class="avatar-img" />
          <div v-else class="avatar-fallback">{{ (user.nickname || user.username)[0] }}</div>
        </div>
        <div class="user-info">
          <h2 class="nickname">{{ user.nickname }}</h2>
          <div class="username">@{{ user.username }}</div>
          <div class="meta-tags">
            <span v-if="user.school" class="meta-tag">🏫 {{ user.school }}</span>
            <span v-if="user.phone" class="meta-tag">📱 {{ user.phone }}</span>
            <span class="meta-tag credit">⭐ 信用分 {{ user.creditScore }}</span>
            <span class="meta-tag">📅 注册于 {{ user.createdAt?.slice(0, 10) }}</span>
          </div>
        </div>
        <button class="btn btn-outline" @click="startEdit">编辑资料</button>
      </div>

      <!-- 快捷入口 -->
      <div class="quick-links">
        <router-link to="/publish" class="quick-item card">
          <span class="qi-icon">➕</span>
          <span>发布商品</span>
        </router-link>
        <router-link to="/my/items" class="quick-item card">
          <span class="qi-icon">📦</span>
          <span>我发布的</span>
        </router-link>
        <router-link to="/my/orders" class="quick-item card">
          <span class="qi-icon">🛒</span>
          <span>我的订单</span>
        </router-link>
        <router-link to="/my/favorites" class="quick-item card">
          <span class="qi-icon">❤️</span>
          <span>我的收藏</span>
        </router-link>
      </div>

      <!-- 编辑资料弹窗 -->
      <div v-if="editing" class="modal-overlay" @click.self="editing=false">
        <div class="modal card">
          <div class="modal-header">
            <h3>编辑个人资料</h3>
            <button class="close-btn" @click="editing=false">✕</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label class="form-label">昵称</label>
              <input v-model="form.nickname" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">手机号</label>
              <input v-model="form.phone" class="form-input" placeholder="选填" />
            </div>
            <div class="form-group">
              <label class="form-label">所在学校</label>
              <input v-model="form.school" class="form-input" placeholder="选填" />
            </div>
            <div class="form-group">
              <label class="form-label">头像 URL</label>
              <input v-model="form.avatar" class="form-input" placeholder="图片链接（选填）" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-ghost" @click="editing=false">取消</button>
            <button class="btn btn-primary" :disabled="loading" @click="saveEdit">
              {{ loading ? '保存中…' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.my-page { padding: 24px 20px 60px; display: flex; flex-direction: column; gap: 20px; }

.my-header {
  display: flex; align-items: center; gap: 24px;
  padding: 28px;
}
@media (max-width: 600px) {
  .my-header { flex-direction: column; text-align: center; }
}

.avatar-large { flex-shrink: 0; }
.avatar-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; }
.avatar-fallback {
  width: 80px; height: 80px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 32px; font-weight: 700;
}

.user-info { flex: 1; }
.nickname { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
.username { font-size: 14px; color: var(--text-muted); margin-bottom: 10px; }
.meta-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.meta-tag {
  font-size: 12px; padding: 3px 10px;
  background: var(--bg); border-radius: 20px;
  color: var(--text-muted); border: 1px solid var(--border);
}
.meta-tag.credit { color: var(--accent); border-color: #fde68a; background: #fefce8; }

.quick-links {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
}
@media (max-width: 600px) { .quick-links { grid-template-columns: repeat(2, 1fr); } }
.quick-item {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 8px; padding: 24px 16px;
  font-size: 14px; font-weight: 500;
  text-decoration: none; color: var(--text);
  transition: transform 0.2s, box-shadow 0.2s;
}
.quick-item:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.qi-icon { font-size: 28px; }

/* 弹窗 */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  z-index: 2000; display: flex; align-items: center; justify-content: center; padding: 20px;
}
.modal { width: 100%; max-width: 420px; }
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 20px; border-bottom: 1px solid var(--border);
}
.modal-header h3 { font-size: 17px; font-weight: 700; }
.close-btn { background: none; border: none; font-size: 18px; cursor: pointer; color: var(--text-muted); }
.modal-body { padding: 20px; }
.modal-footer {
  display: flex; gap: 10px; justify-content: flex-end;
  padding: 14px 20px; border-top: 1px solid var(--border);
}
</style>
