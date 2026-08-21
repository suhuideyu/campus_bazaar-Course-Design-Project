import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  { path: '/', component: () => import('../views/HomeView.vue') },
  { path: '/item/:id', component: () => import('../views/ItemDetailView.vue') },
  { path: '/login', component: () => import('../views/LoginView.vue') },
  { path: '/register', component: () => import('../views/RegisterView.vue') },
  { path: '/publish', component: () => import('../views/PublishView.vue'), meta: { requiresAuth: true } },
  { path: '/my', component: () => import('../views/MyView.vue'), meta: { requiresAuth: true } },
  { path: '/my/items', component: () => import('../views/MyItemsView.vue'), meta: { requiresAuth: true } },
  { path: '/my/orders', component: () => import('../views/MyOrdersView.vue'), meta: { requiresAuth: true } },
  { path: '/my/favorites', component: () => import('../views/MyFavoritesView.vue'), meta: { requiresAuth: true } },
  { path: '/edit/:id', component: () => import('../views/EditItemView.vue'), meta: { requiresAuth: true } },
  { path: '/admin', component: () => import('../views/AdminView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/seller/:sellerId', component: () => import('../views/SellerItemsView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const userStore = useUserStore()
    if (!userStore.isLoggedIn()) {
      return { path: '/login', query: { redirect: to.fullPath } }
    }
    if (to.meta.requiresAdmin && userStore.user.role !== 1) {
      return { path: '/' }
    }
  }
})

export default router
