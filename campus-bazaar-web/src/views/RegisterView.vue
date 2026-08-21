<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../api/index'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  nickname: '',
  phone: '',
  school: ''
})

const loading = ref(false)
const error = ref('')

async function handleRegister() {
  error.value = ''
  const { username, password, confirmPassword, nickname } = form.value

  if (!username || !password || !nickname) {
    error.value = '用户名、密码、昵称不能为空'
    return
  }
  if (password.length < 6) {
    error.value = '密码长度不能少于6位'
    return
  }
  if (password !== confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }

  loading.value = true
  try {
    // ✅ 只提交后端需要的字段，不额外传 confirmPassword
    const submitData = {
      username: form.value.username,
      password: form.value.password,
      nickname: form.value.nickname,
      phone: form.value.phone,
      school: form.value.school
    }

    await userApi.register(submitData)
    const res = await userApi.login({ username, password })
    userStore.setUser(res.data)

    router.push('/')
    window.$toast?.('注册成功！')
  } catch (e) {
    console.error(e)
    error.value = e.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card card">
      <div class="auth-logo">
        <span class="logo-icon">🎒</span>
        <span class="logo-text">校园集市</span>
      </div>
      <h2 class="auth-title">创建账号</h2>
      <p class="auth-sub">加入校园集市，开启二手交易</p>

      <form @submit.prevent="handleRegister">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">用户名 <span class="req">*</span></label>
            <input v-model="form.username" class="form-input" placeholder="登录用，不可更改" />
          </div>
          <div class="form-group">
            <label class="form-label">昵称 <span class="req">*</span></label>
            <input v-model="form.nickname" class="form-input" placeholder="显示给其他用户" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">密码 <span class="req">*</span></label>
            <input v-model="form.password" class="form-input" type="password" placeholder="至少6位" />
          </div>
          <div class="form-group">
            <label class="form-label">确认密码 <span class="req">*</span></label>
            <input v-model="form.confirmPassword" class="form-input" type="password" placeholder="再次输入密码" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label">手机号</label>
            <input v-model="form.phone" class="form-input" placeholder="选填" />
          </div>
          <div class="form-group">
            <label class="form-label">所在学校</label>
            <input v-model="form.school" class="form-input" placeholder="选填" />
          </div>
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" class="btn btn-primary btn-block btn-lg" :disabled="loading">
          {{ loading ? '注册中…' : '立即注册' }}
        </button>
      </form>

      <div class="auth-footer">
        已有账号？
        <router-link to="/login" class="link">去登录</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: calc(100vh - var(--navbar-h));
  display: flex; align-items: center; justify-content: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}
.auth-card { width: 100%; max-width: 520px; padding: 40px 36px; text-align: center; }
.auth-logo { display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 20px; }
.logo-icon { font-size: 28px; }
.logo-text { font-size: 22px; font-weight: 800; color: var(--primary); }
.auth-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.auth-sub { font-size: 14px; color: var(--text-muted); margin-bottom: 24px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
@media (max-width: 480px) { .form-row { grid-template-columns: 1fr; } }
.error-msg {
  color: var(--danger); font-size: 13px;
  background: #fee2e2; border-radius: 6px;
  padding: 8px 12px; margin-bottom: 12px;
  text-align: left;
}
.req { color: var(--danger); }
.auth-footer { margin-top: 20px; font-size: 14px; color: var(--text-muted); }
.link { color: var(--primary); font-weight: 600; }
</style>