<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Toast from './components/Toast.vue'

// 全局 toast
const toasts = ref([])

function showToast(msg, type = 'success') {
  const id = Date.now()
  toasts.value.push({ id, msg, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 3000)
}

// 挂载到 window 方便全局调用
window.$toast = showToast
</script>

<template>
  <Navbar />
  <main class="main-content">
    <RouterView />
  </main>
  <div class="toast-container">
    <div
      v-for="t in toasts"
      :key="t.id"
      class="toast"
      :class="t.type === 'error' ? 'toast-error' : 'toast-success'"
    >{{ t.msg }}</div>
  </div>
</template>

<style>
.main-content {
  flex: 1;
  padding-top: var(--navbar-h);
}
</style>
