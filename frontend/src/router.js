import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

// 路由配置
const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/LoginPage/LoginPage.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('./pages/RegisterPage/RegisterPage.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/channel',
    name: 'Channel',
    component: () => import('./pages/ChannelPage/ChannelPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('./pages/AdminPage/AdminPage.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 需要登录的页面
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // 需要管理员权限的页面
  if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
    next('/channel')
    return
  }

  // 已登录用户不能访问登录/注册页
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/channel')
    return
  }

  next()
})

export default router
