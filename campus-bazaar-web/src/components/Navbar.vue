<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { userApi } from '../api/index'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const menuOpen = ref(false)

const user = computed(() => userStore.user)

async function handleLogout() {
  try { await userApi.logout() } catch {}
  userStore.logout()
  router.push('/')
  menuOpen.value = false
}

function goLogin() { router.push({ path: '/login', query: { redirect: route.fullPath } }) }
function goPublish() { router.push('/publish') }
</script>

<template>
  <nav class="navbar">
    <div class="container nav-inner">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <span class="logo-icon">🎒</span>
        <span class="logo-text">校园集市</span>
      </router-link>

      <!-- 搜索框（桌面端） -->
      <form class="nav-search" @submit.prevent="$router.push({ path: '/', query: { keyword: searchVal } })">
        <input v-model="searchVal" class="nav-search-input" type="text" placeholder="搜索二手商品…" />
        <button type="submit" class="nav-search-btn">🔍</button>
      </form>

      <!-- 右侧操作 -->
      <div class="nav-actions">
        <button v-if="user" class="btn btn-primary btn-sm" @click="goPublish">
          + 发布
        </button>
        <button v-else class="btn btn-primary btn-sm" @click="goLogin">
          登录
        </button>

        <!-- 用户头像/菜单 -->
        <div v-if="user" class="user-menu" @click.stop="menuOpen = !menuOpen">
          <div class="avatar-wrap">
            <img v-if="user.avatar" :src="user.avatar" class="avatar" />
            <div v-else class="avatar-placeholder">{{ (user.nickname || user.username)[0] }}</div>
          </div>
          <!-- 下拉菜单 -->
          <div v-if="menuOpen" class="dropdown" @click.stop>
            <div class="dropdown-header">
              <strong>{{ user.nickname }}</strong>
              <span class="credit">信用分 {{ user.creditScore }}</span>
            </div>
            <router-link to="/my" class="dropdown-item" @click="menuOpen=false">👤 我的主页</router-link>
            <router-link to="/my/items" class="dropdown-item" @click="menuOpen=false">📦 我发布的</router-link>
            <router-link to="/my/orders" class="dropdown-item" @click="menuOpen=false">🛒 我的订单</router-link>
            <router-link to="/my/favorites" class="dropdown-item" @click="menuOpen=false">❤️ 我的收藏</router-link>
            <router-link v-if="user.role === 1" to="/admin" class="dropdown-item" @click="menuOpen=false">⚙️ 管理员</router-link>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item danger" @click="handleLogout">退出登录</button>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <!-- 点击外部关闭菜单 -->
  <div v-if="menuOpen" class="overlay" @click="menuOpen=false"></div>
</template>

<script>
export default { data: () => ({ searchVal: '' }) }
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--navbar-h);
  background: #fff;
  border-bottom: 1px solid var(--border);
  z-index: 1000;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.nav-inner {
  display: flex;
  align-items: center;
  height: 100%;
  gap: 16px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  flex-shrink: 0;
}
.logo-icon { font-size: 22px; }
.logo-text {
  font-size: 17px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: -0.3px;
}
.nav-search {
  flex: 1;
  max-width: 420px;
  display: flex;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  transition: border-color 0.2s;
}
.nav-search:focus-within { border-color: var(--primary); }
.nav-search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0 12px;
  font-size: 14px;
  background: transparent;
}
.nav-search-btn {
  padding: 0 14px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}
.user-menu { position: relative; cursor: pointer; }
.avatar-wrap { width: 36px; height: 36px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; }
.avatar-placeholder {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 15px;
}
.dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 200px;
  background: #fff;
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
  overflow: hidden;
  z-index: 1001;
}
.dropdown-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 2px;
}
.credit { font-size: 12px; color: var(--primary); }
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  font-size: 14px;
  color: var(--text);
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  transition: background 0.15s;
  text-decoration: none;
}
.dropdown-item:hover { background: var(--bg); }
.dropdown-item.danger { color: var(--danger); }
.dropdown-divider { height: 1px; background: var(--border); }
.overlay {
  position: fixed; inset: 0; z-index: 999;
}
@media (max-width: 600px) {
  .nav-search { display: none; }
}
</style>
