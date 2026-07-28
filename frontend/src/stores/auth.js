import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  // 登录
  async function login(username, password) {
    try {
      const response = await api.post('/api/auth/login', {
        username,
        password
      })

      const data = response.data

      // 保存 Token 和用户信息
      token.value = data.access_token
      user.value = {
        id: data.id,
        username: data.username,
        nickname: data.nickname,
        role: data.role,
        avatar: data.avatar
      }

      // 持久化到 localStorage
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(user.value))

      return { success: true, role: data.role }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '登录失败'
      }
    }
  }

  // 注册
  async function register(username, password, nickname) {
    try {
      await api.post('/api/auth/register', {
        username,
        password,
        nickname
      })
      return { success: true }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || '注册失败'
      }
    }
  }

  // 登出
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 更新用户信息
  function updateUser(userData) {
    user.value = { ...user.value, ...userData }
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    updateUser
  }
})
