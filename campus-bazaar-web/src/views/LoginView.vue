<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { userApi } from '../api/index'
import { useUserStore } from '../stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const form = ref({ username: '', password: '' })
const loading = ref(false)

async function handleLogin() {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请填写用户名和密码'); return
  }
  loading.value = true
  try {
    const res = await userApi.login(form.value)
    userStore.setUser(res.data)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
    ElMessage.success('登录成功，欢迎回来 ' + res.data.nickname)
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <el-card class="auth-card" shadow="always">
      <div class="auth-logo">
        <span class="logo-emoji">🎒</span>
        <span class="logo-name">校园集市</span>
      </div>
      <h2 class="auth-title">欢迎回来</h2>
      <p class="auth-sub">登录你的校园集市账号</p>

      <el-form :model="form" label-position="top" size="large" @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" :prefix-icon="User" clearable />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" :prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-button type="primary" size="large" style="width:100%;margin-top:8px" :loading="loading" @click="handleLogin" round>
          {{ loading ? '登录中…' : '登录' }}
        </el-button>
      </el-form>

      <div class="auth-footer">
        还没有账号？<router-link to="/register" class="link">立即注册</router-link>
      </div>

      <el-divider>测试账号</el-divider>
      <div class="test-hint">
        <el-tag type="info" size="small">zhangsan</el-tag>
        <span> / </span>
        <el-tag type="info" size="small">123456</el-tag>
        <el-button link size="small" @click="form.username='zhangsan';form.password='123456'">一键填入</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { User, Lock } from '@element-plus/icons-vue'
export default { setup() { return { User, Lock } } }
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - var(--navbar-h));
  display: flex; align-items: center; justify-content: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #fff7ed 0%, #fef3c7 100%);
}
.auth-card { width: 100%; max-width: 420px; border-radius: 16px; }
:deep(.el-card__body) { padding: 36px; }
.auth-logo { display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 20px; }
.logo-emoji { font-size: 30px; }
.logo-name { font-size: 22px; font-weight: 800; color: var(--primary); }
.auth-title { font-size: 22px; font-weight: 700; text-align: center; margin-bottom: 4px; }
.auth-sub { font-size: 14px; color: var(--text-muted); text-align: center; margin-bottom: 24px; }
.auth-footer { margin-top: 18px; font-size: 14px; color: var(--text-muted); text-align: center; }
.link { color: var(--primary); font-weight: 600; }
.test-hint { text-align: center; font-size: 13px; color: var(--text-muted); }
</style>
