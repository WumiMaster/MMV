<template>
  <div class="login-container">
    <div class="glass-card auth-card animate-slide-up">
      <div class="auth-logo">
        <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      </div>
      <div class="auth-title">欢迎回来</div>
      <div class="auth-subtitle">登录你的语音频道账号</div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-toast">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input
            ref="usernameInput"
            v-model="username"
            type="text"
            class="glass-input"
            placeholder="请输入用户名"
            required
            @keydown="handleUsernameKeydown"
          />
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <div class="input-wrapper">
            <input
              ref="passwordInput"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="glass-input"
              placeholder="请输入密码"
              required
              @keydown="handlePasswordKeydown"
            />
            <button
              type="button"
              class="eye-btn"
              @click="showPassword = !showPassword"
            >
              <!-- 隐藏密码：闭眼图标 -->
              <svg v-if="showPassword" class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z"></path>
                <circle cx="12" cy="12" r="3"></circle>
                <line x1="2" y1="2" x2="22" y2="22"></line>
              </svg>
              <!-- 显示密码：睁眼图标 -->
              <svg v-else class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </button>
          </div>
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>

      <div class="auth-link">
        还没有账号？
        <router-link to="/register">去注册 →</router-link>
      </div>
    </div>

    <!-- 管理员选择弹窗 -->
    <div v-if="showAdminChoice" class="modal-overlay animate-overlay-in" @click.self="showAdminChoice = false">
      <div class="glass-card modal animate-modal-in">
        <div class="modal-header">
          <div class="modal-title">检测到管理员账号</div>
        </div>

        <p class="modal-desc">
          你的账号拥有管理员权限，请选择要进入的页面。
        </p>

        <div class="modal-actions">
          <button class="btn-primary" @click="goToChannel">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
              <line x1="12" y1="19" x2="12" y2="23"></line>
              <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
            进入频道页面
          </button>
          <button class="btn-secondary" @click="goToAdmin">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            进入管理后台
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 输入框引用
const usernameInput = ref(null)
const passwordInput = ref(null)

// 用户名输入框键盘事件
function handleUsernameKeydown(event) {
  if (event.key === 'ArrowDown' || event.key === 'Enter') {
    event.preventDefault()
    passwordInput.value?.focus()
  }
}

// 密码输入框键盘事件
function handlePasswordKeydown(event) {
  if (event.key === 'ArrowUp') {
    event.preventDefault()
    usernameInput.value?.focus()
  }
}

// 表单数据
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

// 管理员选择弹窗
const showAdminChoice = ref(false)

// 登录处理
async function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  const result = await authStore.login(username.value, password.value)

  if (result.success) {
    // 判断是否为管理员
    if (result.role === 'admin') {
      showAdminChoice.value = true
    } else {
      router.push('/channel')
    }
  } else {
    errorMessage.value = result.message
  }

  loading.value = false
}

// 跳转频道页
function goToChannel() {
  showAdminChoice.value = false
  router.push('/channel')
}

// 跳转管理后台
function goToAdmin() {
  showAdminChoice.value = false
  router.push('/admin')
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  z-index: 1;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  text-align: center;
}

.auth-logo {
  width: 72px;
  height: 72px;
  border-radius: 24px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(255, 158, 181, 0.4);
}

.logo-icon {
  width: 36px;
  height: 36px;
  color: white;
}

.eye-icon {
  width: 20px;
  height: 20px;
  color: #888;
}

.auth-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #2d2d2d;
}

.auth-subtitle {
  color: #888;
  margin-bottom: 32px;
  font-size: 14px;
}

.error-toast {
  background: rgba(255, 107, 107, 0.08);
  border: 1px solid rgba(255, 107, 107, 0.25);
  color: #e05555;
  padding: 12px 16px;
  border-radius: 14px;
  margin-bottom: 20px;
  font-size: 14px;
  animation: slideUp 0.3s ease;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #555;
}

.input-wrapper {
  position: relative;
}

/* 隐藏浏览器自带的密码显示按钮 */
.input-wrapper input::-ms-reveal,
.input-wrapper input::-ms-clear {
  display: none;
}

.input-wrapper input::-webkit-textfield-decoration-container {
  display: none !important;
}

.eye-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  z-index: 10;
}

.btn-icon {
  width: 18px;
  height: 18px;
  vertical-align: middle;
  margin-right: 6px;
  display: inline-block;
}

.auth-link {
  margin-top: 20px;
  font-size: 14px;
  color: #888;
}

.auth-link a {
  color: #7ED7A7;
  text-decoration: none;
  font-weight: 600;
}

.auth-link a:hover {
  text-decoration: underline;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  width: 90%;
  max-width: 400px;
  padding: 28px;
  text-align: center;
}

.modal-header {
  margin-bottom: 16px;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
}

.modal-desc {
  color: #666666;
  margin-bottom: 24px;
  line-height: 1.6;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-actions .btn-primary,
.modal-actions .btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
