<template>
  <!-- 设置弹窗 -->
  <Teleport to="body">
    <div class="modal-overlay animate-overlay-in" @click.self="$emit('close')">
      <div class="modal-container animate-modal-in">
        <div class="modal-header">
          <h3>设置</h3>
          <button class="close-btn" @click="$emit('close')">×</button>
        </div>

        <div class="modal-body">
            <!-- 头像区域（居中） -->
            <div class="avatar-section">
              <div class="avatar-wrapper" @click="triggerAvatarInput">
                <div class="avatar-preview">
                  <img v-if="avatarPreview" :src="avatarPreview" alt="头像预览" />
                  <img v-else-if="authStore.user?.avatar" :src="authStore.user.avatar" alt="当前头像" />
                  <div v-else class="avatar-placeholder">
                    {{ authStore.user?.nickname?.charAt(0) || '?' }}
                  </div>
                </div>
                <div class="avatar-overlay">
                  <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>点击更换</span>
                </div>
              </div>
              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                @change="handleAvatarChange"
                style="display: none"
              />
            </div>

            <!-- 昵称设置 -->
            <div class="settings-section">
              <h4>个人信息</h4>
              <div class="setting-item">
                <label>昵称</label>
                <div class="current-nickname">
                  当前昵称：{{ authStore.user?.nickname || '未设置' }}
                </div>
                <input
                  v-model="nickname"
                  type="text"
                  placeholder="输入新昵称"
                  class="setting-input"
                />
              </div>
            </div>

            <!-- 音频设置 -->
            <div class="settings-section">
              <h4>音频设置</h4>
              <div class="setting-item">
                <label>麦克风</label>
                <select v-model="selectedMic" class="setting-select">
                  <option value="">选择麦克风</option>
                  <option v-for="device in audioDevices.mics" :key="device.deviceId" :value="device.deviceId">
                    {{ device.label || `麦克风 ${device.deviceId.slice(0, 8)}` }}
                  </option>
                </select>
              </div>
              <div class="setting-item">
                <label>扬声器</label>
                <select v-model="selectedSpeaker" class="setting-select">
                  <option value="">选择扬声器</option>
                  <option v-for="device in audioDevices.speakers" :key="device.deviceId" :value="device.deviceId">
                    {{ device.label || `扬声器 ${device.deviceId.slice(0, 8)}` }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="$emit('close')">取消</button>
            <button class="btn btn-primary" @click="saveSettings" :disabled="saving">
              {{ saving ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
/**
 * 设置弹窗组件
 * 用户可以修改昵称、头像和音频设备设置
 */

import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const emit = defineEmits(['close'])
const authStore = useAuthStore()

// 个人信息
const nickname = ref(authStore.user?.nickname || '')
const avatarInput = ref(null)
const avatarFile = ref(null)
const avatarPreview = ref(null)

// 音频设备
const selectedMic = ref('')
const selectedSpeaker = ref('')
const audioDevices = ref({ mics: [], speakers: [] })

// 状态
const saving = ref(false)

// 触发头像上传
function triggerAvatarInput() {
  avatarInput.value?.click()
}

// 处理头像选择
function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (file) {
    avatarFile.value = file
    avatarPreview.value = URL.createObjectURL(file)
  }
}

// 获取音频设备列表
async function getAudioDevices() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    stream.getTracks().forEach(track => track.stop())

    const devices = await navigator.mediaDevices.enumerateDevices()
    audioDevices.value = {
      mics: devices.filter(d => d.kind === 'audioinput'),
      speakers: devices.filter(d => d.kind === 'audiooutput')
    }

    if (audioDevices.value.mics.length > 0 && !selectedMic.value) {
      selectedMic.value = audioDevices.value.mics[0].deviceId
    }
    if (audioDevices.value.speakers.length > 0 && !selectedSpeaker.value) {
      selectedSpeaker.value = audioDevices.value.speakers[0].deviceId
    }
  } catch (error) {
    console.error('获取音频设备失败:', error)
  }
}

// 保存设置
async function saveSettings() {
  saving.value = true

  try {
    // 更新昵称
    if (nickname.value && nickname.value !== authStore.user?.nickname) {
      await api.put('/api/auth/profile', { nickname: nickname.value })
      authStore.updateUser({ nickname: nickname.value })
    }

    // 上传头像
    if (avatarFile.value) {
      const formData = new FormData()
      formData.append('file', avatarFile.value)
      const response = await api.post('/api/auth/avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      authStore.updateUser({ avatar: response.data.avatar })
    }

    emit('close')
  } catch (error) {
    console.error('保存设置失败:', error)
    alert('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  getAudioDevices()
})
</script>

<style scoped>
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

.modal-container {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  width: 400px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.9);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  transition: all 0.15s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  max-height: 60vh;
}

/* 头像区域 */
.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.avatar-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
}

.avatar-preview {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255, 158, 181, 0.3);
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  color: white;
  font-size: 32px;
  font-weight: 600;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  border-radius: 50%;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.avatar-overlay svg {
  width: 24px;
  height: 24px;
  margin-bottom: 4px;
}

.avatar-overlay span {
  font-size: 10px;
  color: white;
}

/* 设置区域 */
.settings-section {
  margin-bottom: 24px;
}

.settings-section:last-child {
  margin-bottom: 0;
}

.settings-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #666;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.setting-item {
  margin-bottom: 16px;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-item label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 6px;
}

.current-nickname {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
  padding: 6px 10px;
  background: rgba(255, 240, 245, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(220, 210, 218, 0.3);
}

.setting-input,
.setting-select {
  width: 100%;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
  box-sizing: border-box;
}

.setting-input:focus,
.setting-select:focus {
  border-color: #FF9EB5;
  box-shadow: 0 0 0 3px rgba(255, 158, 181, 0.2);
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 16px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.btn {
  padding: 10px 20px;
  border-radius: 10px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-secondary {
  background: rgba(0, 0, 0, 0.05);
  color: #666;
}

.btn-secondary:hover {
  background: rgba(0, 0, 0, 0.08);
}

.btn-primary {
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 158, 181, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
</style>
