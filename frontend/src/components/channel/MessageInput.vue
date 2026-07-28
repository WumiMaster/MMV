<template>
  <!-- 消息输入组件 -->
  <div class="message-input">
    <!-- 图片预览 -->
    <div v-if="imagePreview" class="image-preview">
      <img :src="imagePreview" alt="预览" />
      <button class="remove-btn" @click="removeImage">×</button>
    </div>

    <!-- 上传中提示 -->
    <div v-if="uploading" class="uploading-tip">
      上传中...
    </div>

    <div class="input-row">
      <div class="input-actions">
        <button class="action-btn" @click="triggerImageUpload" title="上传图片">
          <svg class="action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </button>
        <input
          ref="imageInput"
          type="file"
          accept="image/*"
          style="display: none"
          @change="handleImageUpload"
        />
      </div>

      <textarea
        v-model="content"
        class="input-field"
        placeholder="输入消息... (Enter 发送，Shift+Enter 换行)"
        @keydown="handleKeyDown"
        @paste="handlePaste"
        rows="1"
        ref="textareaRef"
      ></textarea>

      <button class="send-btn" @click="sendMessage" :disabled="!canSend">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
/**
 * 消息输入组件
 * 支持文字输入、图片上传、粘贴图片
 */

import { ref, computed, nextTick } from 'vue'
import api from '../../api'

const props = defineProps({
  subChannelId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['send'])

// 输入内容
const content = ref('')
const imageInput = ref(null)
const imageFile = ref(null)
const imagePreview = ref(null)
const imageUrl = ref(null)
const uploading = ref(false)
const textareaRef = ref(null)

// 是否可发送
const canSend = computed(() => {
  return (content.value.trim() || imageUrl.value) && !uploading.value
})

// 触发图片上传
function triggerImageUpload() {
  imageInput.value.click()
}

// 处理图片上传
async function handleImageUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }

  // 验证文件大小（最大 10MB）
  if (file.size > 10 * 1024 * 1024) {
    alert('图片大小不能超过 10MB')
    return
  }

  // 显示预览
  imageFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)

  // 上传图片
  await uploadImage(file)
}

// 上传图片到服务器
async function uploadImage(file) {
  uploading.value = true

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    imageUrl.value = response.data.image_url
  } catch (error) {
    console.error('图片上传失败:', error)
    alert('图片上传失败，请重试')
    removeImage()
  } finally {
    uploading.value = false
  }
}

// 移除图片
function removeImage() {
  imageFile.value = null
  imagePreview.value = null
  imageUrl.value = null
  if (imageInput.value) {
    imageInput.value.value = ''
  }
}

// 处理粘贴事件
async function handlePaste(event) {
  const items = event.clipboardData?.items
  if (!items) return

  for (const item of items) {
    if (item.type.startsWith('image/')) {
      event.preventDefault()
      const file = item.getAsFile()
      if (file) {
        imageFile.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
        await uploadImage(file)
      }
      break
    }
  }
}

// 处理键盘事件
function handleKeyDown(event) {
  // Enter 发送，Shift+Enter 换行
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

// 发送消息
async function sendMessage() {
  if (!canSend.value) return

  const messageData = {
    content: content.value.trim() || null,
    image_url: imageUrl.value || null
  }

  emit('send', messageData)

  // 清空输入
  content.value = ''
  removeImage()

  // 聚焦输入框
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.focus()
    }
  })
}
</script>

<style scoped>
.message-input {
  padding: 12px 16px;
  border-top: 1px solid rgba(220, 200, 210, 0.45);
  background: rgba(255, 242, 250, 0.4);
  position: relative;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.03);
}

/* 输入行：图片按钮 + 输入框 + 发送按钮 */
.input-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.input-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.action-btn {
  width: 40px;
  height: 40px;
  border: 1px solid rgba(200, 190, 195, 0.5);
  background: rgba(255, 240, 248, 0.6);
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.action-icon {
  width: 20px;
  height: 20px;
}

.action-btn:hover {
  background: rgba(255, 220, 235, 0.7);
  border-color: rgba(255, 200, 220, 0.65);
  box-shadow: 0 3px 10px rgba(255, 158, 181, 0.2);
}

.input-field {
  flex: 1;
  min-height: 40px;
  max-height: 120px;
  padding: 10px 14px;
  border: 1px solid rgba(200, 190, 198, 0.5);
  border-radius: 14px;
  background: rgba(255, 242, 250, 0.55);
  font-size: 14px;
  resize: none;
  outline: none;
  font-family: inherit;
  line-height: 1.4;
  color: #333;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.input-field::placeholder {
  color: #b0b0b0;
}

.input-field:focus {
  border-color: #6BC99A;
  background: rgba(255, 248, 252, 0.85);
  box-shadow: 0 0 0 3px rgba(126, 215, 167, 0.22), 0 3px 10px rgba(0, 0, 0, 0.06);
}

.send-btn {
  height: 40px;
  padding: 0 24px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #FF9EB5, #FFB8CC);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, box-shadow 0.2s ease;
  flex-shrink: 0;
  white-space: nowrap;
  box-shadow: 0 4px 14px rgba(255, 158, 181, 0.4);
}

.send-btn:hover:not(:disabled) {
  box-shadow: 0 6px 20px rgba(255, 158, 181, 0.5);
  background: linear-gradient(135deg, #FFA8BD, #FFC0D2);
}

.send-btn:active:not(:disabled) {
  box-shadow: 0 3px 10px rgba(255, 158, 181, 0.38);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: 0 2px 8px rgba(255, 158, 181, 0.25);
}

/* 图片预览 */
.image-preview {
  position: absolute;
  bottom: 100%;
  left: 16px;
  margin-bottom: 8px;
  background: rgba(255, 248, 252, 0.95);
  border: 1px solid rgba(220, 200, 210, 0.5);
  border-radius: 14px;
  padding: 8px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.image-preview img {
  max-width: 200px;
  max-height: 150px;
  border-radius: 10px;
  display: block;
}

.image-preview .remove-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border: none;
  background: #FF6B6B;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  line-height: 1;
  box-shadow: 0 2px 6px rgba(255, 107, 107, 0.3);
}

.uploading-tip {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
</style>
