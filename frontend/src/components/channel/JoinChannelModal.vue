<template>
  <!-- 加入频道弹窗 -->
  <div class="modal-overlay animate-overlay-in" @click.self="$emit('close')">
    <div class="glass-card modal animate-modal-in">
      <div class="modal-header">
        <div class="modal-title">加入频道</div>
        <button class="modal-close" @click="$emit('close')">×</button>
      </div>

      <div v-if="errorMessage" class="error-toast">
        {{ errorMessage }}
      </div>

      <div v-if="successMessage" class="success-toast">
        {{ successMessage }}
      </div>

      <div class="form-group">
        <label class="form-label">频道 ID</label>
        <input
          v-model="channelId"
          type="text"
          class="glass-input"
          placeholder="请输入频道 ID"
          @keyup.enter="handleJoin"
        />
      </div>

      <div class="modal-footer">
        <button class="btn-cancel" @click="$emit('close')">取消</button>
        <button class="btn-primary" @click="handleJoin" :disabled="loading || !channelId.trim()">
          {{ loading ? '加入中...' : '加入' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 加入频道弹窗组件
 * 用户输入频道ID加入频道
 */

import { ref } from 'vue'
import api from '../../api'

const emit = defineEmits(['close', 'joined'])

const channelId = ref('')
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

async function handleJoin() {
  if (!channelId.value.trim()) return

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await api.post('/api/channels/join', {
      channel_id: channelId.value.trim()
    })

    successMessage.value = '加入成功！'

    // 通知父组件
    setTimeout(() => {
      emit('joined', response.data)
    }, 500)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '加入失败，请检查频道ID'
  } finally {
    loading.value = false
  }
}
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

.modal {
  width: 90%;
  max-width: 400px;
  padding: 28px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.15s;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: scale(1.1);
}

.error-toast {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  color: #FF6B6B;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 16px;
  font-size: 14px;
}

.success-toast {
  background: rgba(81, 207, 102, 0.1);
  border: 1px solid rgba(81, 207, 102, 0.3);
  color: #51CF66;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 16px;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
}

.modal-footer {
  display: flex;
  gap: 12px;
}

.modal-footer button {
  flex: 1;
}

.btn-primary {
  height: 48px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #FF9EB5, #FFD1E0);
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-primary:hover:not(:disabled) {
  transform: scale(1.03);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  height: 48px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.5);
  border-radius: 14px;
  cursor: pointer;
  font-size: 15px;
  transition: all 0.15s;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.8);
}
</style>
