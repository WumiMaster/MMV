<template>
  <div class="register-container">
    <div class="glass-card auth-card animate-slide-up">
      <div class="auth-logo">
        <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      </div>
      <div class="auth-title">创建账号</div>
      <div class="auth-subtitle">加入精简语音频道</div>

      <!-- 头像上传 -->
      <div class="avatar-upload" @click="triggerFileInput">
        <div v-if="avatarPreview" class="avatar-preview">
          <img :src="avatarPreview" alt="头像预览" />
        </div>
        <div v-else class="avatar-placeholder">
          <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
            <circle cx="12" cy="13" r="4"></circle>
          </svg>
          <div>点击上传头像</div>
        </div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          style="display: none"
          @change="handleAvatarChange"
        />
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-toast">
        {{ errorMessage }}
      </div>

      <!-- 成功提示 -->
      <div v-if="successMessage" class="success-toast">
        {{ successMessage }}
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label">用户名 *</label>
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
          <label class="form-label">密码 *</label>
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

        <div class="form-group">
          <label class="form-label">确认密码 *</label>
          <div class="input-wrapper">
            <input
              ref="confirmPasswordInput"
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="glass-input"
              placeholder="请再次输入密码"
              required
              @keydown="handleConfirmPasswordKeydown"
            />
            <button
              type="button"
              class="eye-btn"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <!-- 隐藏密码：闭眼图标 -->
              <svg v-if="showConfirmPassword" class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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

        <div class="form-group">
          <label class="form-label">昵称 *</label>
          <input
            ref="nicknameInput"
            v-model="nickname"
            type="text"
            class="glass-input"
            placeholder="对外显示的昵称"
            required
            @keydown="handleNicknameKeydown"
          />
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '注册中...' : '注 册' }}
        </button>
      </form>

      <div class="auth-link">
        已有账号？
        <router-link to="/login">去登录 →</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 输入框引用
const usernameInput = ref(null)
const passwordInput = ref(null)
const confirmPasswordInput = ref(null)
const nicknameInput = ref(null)

// 键盘导航
function handleUsernameKeydown(event) {
  if (event.key === 'ArrowDown' || event.key === 'Enter') {
    event.preventDefault()
    passwordInput.value?.focus()
  }
}

function handlePasswordKeydown(event) {
  if (event.key === 'ArrowDown' || event.key === 'Enter') {
    event.preventDefault()
    confirmPasswordInput.value?.focus()
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    usernameInput.value?.focus()
  }
}

function handleConfirmPasswordKeydown(event) {
  if (event.key === 'ArrowDown' || event.key === 'Enter') {
    event.preventDefault()
    nicknameInput.value?.focus()
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    passwordInput.value?.focus()
  }
}

function handleNicknameKeydown(event) {
  if (event.key === 'ArrowUp') {
    event.preventDefault()
    confirmPasswordInput.value?.focus()
  }
}
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const router = useRouter()
const authStore = useAuthStore()

// 表单数据
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const nickname = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// 头像相关
const fileInput = ref(null)
const avatarFile = ref(null)
const avatarPreview = ref(null)

// 触发文件选择
function triggerFileInput() {
  fileInput.value.click()
}

// 处理头像选择
function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    errorMessage.value = '请选择图片文件'
    return
  }

  // 验证文件大小（最大 5MB）
  if (file.size > 5 * 1024 * 1024) {
    errorMessage.value = '图片大小不能超过 5MB'
    return
  }

  avatarFile.value = file

  // 创建预览
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

// 注册处理
async function handleRegister() {
  errorMessage.value = ''
  successMessage.value = ''

  // 验证密码
  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  if (password.value.length < 6) {
    errorMessage.value = '密码长度不能少于 6 位'
    return
  }

  loading.value = true

  const result = await authStore.register(username.value, password.value, nickname.value)

  if (result.success) {
    successMessage.value = '注册成功！2 秒后跳转到登录页...'

    // 如果有头像，上传头像
    if (avatarFile.value) {
      try {
        const formData = new FormData()
        formData.append('file', avatarFile.value)

        // 先登录获取 token
        const loginResult = await authStore.login(username.value, password.value)
        if (loginResult.success) {
          // 上传头像
          await api.post('/api/auth/avatar', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
        }
      } catch (error) {
        console.error('头像上传失败:', error)
      }
    }

    // 跳转登录页
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    errorMessage.value = result.message
  }

  loading.value = false
}
</script>

<style scoped>
.register-container {
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

.upload-icon {
  width: 32px;
  height: 32px;
  color: #999;
  margin-bottom: 8px;
}

.auth-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.auth-subtitle {
  color: #666666;
  margin-bottom: 24px;
  font-size: 14px;
}

.avatar-upload {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px dashed rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.4);
  margin: 0 auto 24px;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
}

.avatar-upload:hover {
  border-color: #7ED7A7;
  background: rgba(255, 255, 255, 0.7);
  transform: scale(1.05);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 12px;
}

.avatar-placeholder .upload-icon {
  width: 28px;
  height: 28px;
  color: #999;
  margin-bottom: 4px;
}

.avatar-preview {
  width: 100%;
  height: 100%;
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.error-toast {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  color: #FF6B6B;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  font-size: 14px;
  animation: slideUp 0.3s ease;
}

.success-toast {
  background: rgba(81, 207, 102, 0.1);
  border: 1px solid rgba(81, 207, 102, 0.3);
  color: #51CF66;
  padding: 12px 16px;
  border-radius: 12px;
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

.auth-link {
  margin-top: 20px;
  font-size: 14px;
  color: #666666;
}

.auth-link a {
  color: #7ED7A7;
  text-decoration: none;
  font-weight: 600;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>
