<template>
  <!-- 聊天窗口 -->
  <div class="chat-window">
    <div class="chat-header">
      <div class="chat-title">
        <span class="icon">#</span>
        {{ subChannelName }}
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="message-list" ref="messageListRef" @scroll="handleScroll">
      <div v-if="loading" class="loading-tip">加载中...</div>
      <div v-if="!loading && messages.length === 0" class="empty-tip">
        还没有消息，发送第一条吧！
      </div>

      <div v-if="hasMore" class="load-more" @click="loadMore">
        加载更多消息
      </div>

      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message-item"
        :class="{ 'is-self': msg.user.id === currentUserId }"
      >
        <div class="message-avatar">
          <img v-if="msg.user.avatar" :src="msg.user.avatar" alt="头像" />
          <span v-else>{{ msg.user.nickname.charAt(0) }}</span>
        </div>
        <div class="message-content">
          <div class="message-header">
            <span class="nickname">{{ msg.user.nickname }}</span>
            <span class="time">{{ formatTime(msg.created_at) }}</span>
          </div>
          <div v-if="msg.content" class="message-text">{{ msg.content }}</div>
          <div v-if="msg.image_url" class="message-image">
            <img :src="msg.image_url" alt="图片" @click="previewImage(msg.image_url)" />
          </div>
        </div>
      </div>
    </div>

    <!-- 新消息提示按钮 -->
    <Transition name="bounce">
      <button
        v-if="showNewMessageHint"
        class="new-message-hint"
        @click="scrollToBottomAndClear"
      >
        <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
        <span v-if="newMessageCount > 0" class="message-count">{{ newMessageCount > 99 ? '99+' : newMessageCount }}</span>
        <span class="hint-text">新消息</span>
      </button>
    </Transition>

    <!-- 消息输入 -->
    <MessageInput
      :sub-channel-id="subChannelId"
      @send="handleSendMessage"
    />

    <!-- 图片预览 -->
    <div v-if="previewUrl" class="image-preview-overlay" @click.self="closePreview">
      <div class="preview-controls">
        <button class="preview-btn" @click="zoomIn" title="放大">+</button>
        <span class="zoom-level">{{ Math.round(zoomLevel * 100) }}%</span>
        <button class="preview-btn" @click="zoomOut" title="缩小">-</button>
        <button class="preview-btn" @click="resetZoom" title="重置">↺</button>
        <button class="preview-btn close" @click="closePreview" title="关闭">✕</button>
      </div>
      <div
        class="preview-image-container"
        @wheel.prevent="handleWheel"
        @mousedown="startDrag"
        @mousemove="onDrag"
        @mouseup="endDrag"
        @mouseleave="endDrag"
        :style="{ cursor: zoomLevel > 1 ? (isDragging ? 'grabbing' : 'grab') : 'default' }"
      >
        <img
          ref="previewImageRef"
          :src="previewUrl"
          alt="预览"
          :style="{
            transform: `translate(calc(-50% + ${panX}px), calc(-50% + ${panY}px)) scale(${zoomLevel})`
          }"
          @load="onImageLoad"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 聊天窗口组件
 * 显示消息列表和输入框
 */

import { ref, watch, nextTick, onMounted } from 'vue'
import api from '../../api'
import MessageInput from './MessageInput.vue'

const props = defineProps({
  subChannelId: {
    type: Number,
    required: true
  },
  subChannelName: {
    type: String,
    default: ''
  },
  currentUserId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['send'])

// 消息数据
const messages = ref([])
const loading = ref(false)
const hasMore = ref(false)
const page = ref(1)
const messageListRef = ref(null)
const previewUrl = ref(null)
const previewImageRef = ref(null)

// 图片预览相关
const zoomLevel = ref(1)
const panX = ref(0)
const panY = ref(0)
const transformOriginX = ref(0)
const transformOriginY = ref(0)
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const dragStartPanX = ref(0)
const dragStartPanY = ref(0)

// 新消息提示相关
const isAtBottom = ref(true)
const newMessageCount = ref(0)
const showNewMessageHint = ref(false)

// 检测是否滚动到底部
function handleScroll() {
  if (!messageListRef.value) return
  const { scrollTop, scrollHeight, clientHeight } = messageListRef.value
  // 距离底部 50px 以内视为在底部
  isAtBottom.value = scrollHeight - scrollTop - clientHeight < 50

  // 如果滚到底部，隐藏提示
  if (isAtBottom.value) {
    showNewMessageHint.value = false
    newMessageCount.value = 0
  }
}

// 滚动到底部并清除提示
function scrollToBottomAndClear() {
  scrollToBottom()
  showNewMessageHint.value = false
  newMessageCount.value = 0
}

// 加载消息
async function loadMessages(append = false) {
  if (loading.value) return
  loading.value = true

  try {
    const response = await api.get(`/api/messages/${props.subChannelId}`, {
      params: {
        page: append ? page.value : 1,
        page_size: 50
      }
    })

    const data = response.data
    if (append) {
      // 加载更多：将旧消息添加到前面
      messages.value = [...data.messages.reverse(), ...messages.value]
    } else {
      // 初始加载：反转顺序（最新的在后面）
      messages.value = data.messages.reverse()
      // 初始加载后滚动到底部
      scrollToBottom()
    }
    hasMore.value = data.has_more
  } catch (error) {
    console.error('加载消息失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多
function loadMore() {
  page.value++
  loadMessages(true)
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
      isAtBottom.value = true
    }
  })
}

// 发送消息
async function handleSendMessage(messageData) {
  try {
    const response = await api.post('/api/messages', {
      sub_channel_id: props.subChannelId,
      content: messageData.content,
      image_url: messageData.image_url
    })

    // 不在本地添加，由父组件统一处理（避免重复显示）
    // 通知父组件（父组件会添加到消息列表并广播WebSocket）
    emit('send', response.data)
  } catch (error) {
    console.error('发送消息失败:', error)
  }
}

// 添加实时消息
function addMessage(message) {
  messages.value.push(message)

  // 如果用户在底部，自动滚动
  if (isAtBottom.value) {
    scrollToBottom()
  } else {
    // 用户不在底部，显示新消息提示
    newMessageCount.value++
    showNewMessageHint.value = true
  }
}

// 格式化时间
function formatTime(timeStr) {
  if (!timeStr) return ''

  // 解析 ISO 格式时间（带时区）
  let date
  if (timeStr.includes('T')) {
    // ISO 8601 格式
    date = new Date(timeStr)
  } else {
    // 兼容旧格式（无时区，假设是 UTC）
    date = new Date(timeStr + 'Z')
  }

  const now = new Date()
  const diff = now - date

  // 今天内只显示时间
  if (diff < 24 * 60 * 60 * 1000 && date.getDate() === now.getDate()) {
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  // 今年显示月日时间
  if (date.getFullYear() === now.getFullYear()) {
    return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }) + ' ' +
           date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  // 其他显示完整日期
  return date.toLocaleDateString('zh-CN') + ' ' +
         date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 预览图片
function previewImage(url) {
  previewUrl.value = url
  // 延迟重置，等待图片加载
  nextTick(() => {
    zoomLevel.value = 1
    panX.value = 0
    panY.value = 0
  })
}

// 关闭预览
function closePreview() {
  previewUrl.value = null
  zoomLevel.value = 1
  panX.value = 0
  panY.value = 0
}

// 图片加载完成
function onImageLoad() {
  // 图片加载完成后，重置为默认状态
  zoomLevel.value = 1
  panX.value = 0
  panY.value = 0
}

// 鼠标滚轮缩放（以鼠标位置为中心）
function handleWheel(event) {
  const container = event.currentTarget
  const rect = container.getBoundingClientRect()
  const mouseX = event.clientX - rect.left
  const mouseY = event.clientY - rect.top

  // 图片中心在容器中的位置
  const centerX = rect.width / 2 + panX.value
  const centerY = rect.height / 2 + panY.value

  // 鼠标相对于图片中心的偏移
  const offsetX = mouseX - centerX
  const offsetY = mouseY - centerY

  const oldZoom = zoomLevel.value
  let newZoom
  if (event.deltaY < 0) {
    newZoom = Math.min(5, oldZoom + 0.2)
  } else {
    newZoom = Math.max(0.2, oldZoom - 0.2)
  }

  // 缩放比例
  const scale = newZoom / oldZoom

  // 调整平移，使鼠标位置保持不变
  panX.value = mouseX - rect.width / 2 - (mouseX - rect.width / 2 - panX.value) * scale
  panY.value = mouseY - rect.height / 2 - (mouseY - rect.height / 2 - panY.value) * scale

  zoomLevel.value = newZoom
}

// 拖拽功能
function startDrag(event) {
  if (zoomLevel.value <= 1) return
  isDragging.value = true
  dragStartX.value = event.clientX
  dragStartY.value = event.clientY
  dragStartPanX.value = panX.value
  dragStartPanY.value = panY.value
  event.preventDefault()
}

function onDrag(event) {
  if (!isDragging.value) return
  const dx = event.clientX - dragStartX.value
  const dy = event.clientY - dragStartY.value
  panX.value = dragStartPanX.value + dx
  panY.value = dragStartPanY.value + dy
}

function endDrag() {
  isDragging.value = false
}

// 按钮缩放（以容器中心为中心）
function zoomIn() {
  const oldZoom = zoomLevel.value
  const newZoom = Math.min(5, oldZoom + 0.25)
  zoomLevel.value = newZoom
}

function zoomOut() {
  const oldZoom = zoomLevel.value
  const newZoom = Math.max(0.2, oldZoom - 0.25)
  zoomLevel.value = newZoom
}

function resetZoom() {
  zoomLevel.value = 1
  panX.value = 0
  panY.value = 0
}

// 当子频道切换时重新加载消息
watch(() => props.subChannelId, (newId, oldId) => {
  if (newId !== oldId) {
    // 清空当前消息
    messages.value = []
    page.value = 1
    hasMore.value = false
    // 加载新消息
    loadMessages()
  }
})

// 组件挂载时加载消息
onMounted(() => {
  if (props.subChannelId) {
    loadMessages()
  }
})

// 暴露方法给父组件
defineExpose({
  addMessage,
  scrollToBottom
})
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: linear-gradient(
    180deg,
    rgba(255, 245, 250, 0.45) 0%,
    rgba(255, 240, 248, 0.35) 100%
  );
  height: 100%;
  min-height: 0;
  position: relative;
}

.chat-header {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(220, 200, 210, 0.45);
  background: rgba(255, 242, 250, 0.4);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.chat-title {
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
}

.chat-title .icon {
  color: #999;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  min-height: 0;
}

.loading-tip,
.empty-tip {
  text-align: center;
  color: #888;
  padding: 40px 0;
  font-size: 14px;
  background: rgba(255, 245, 250, 0.3);
  border-radius: 12px;
  margin: 16px;
}

.load-more {
  text-align: center;
  color: #6BC99A;
  padding: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
}

.load-more:hover {
  text-decoration: underline;
  color: #5ab888;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message-item.is-self {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  flex-shrink: 0;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-content {
  max-width: 70%;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.is-self .message-header {
  flex-direction: row-reverse;
}

.nickname {
  font-size: 13px;
  font-weight: 600;
  color: #444;
}

.time {
  font-size: 11px;
  color: #888;
}

.message-text {
  background: rgba(255, 242, 250, 0.75);
  border: 1px solid rgba(220, 200, 210, 0.5);
  padding: 12px 16px;
  border-radius: 0 16px 16px 16px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  color: #333;
}

.is-self .message-text {
  background: linear-gradient(135deg, rgba(190, 240, 210, 0.65), rgba(210, 248, 225, 0.55));
  border: 1px solid rgba(170, 230, 200, 0.5);
  border-radius: 16px 0 16px 16px;
  box-shadow: 0 2px 8px rgba(126, 215, 167, 0.1);
}

.message-image {
  margin-top: 10px;
}

.message-image img {
  max-width: 300px;
  max-height: 200px;
  border-radius: 14px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid rgba(220, 200, 210, 0.4);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.message-image img:hover {
  transform: scale(1.02);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
}

/* 图片预览 */
.image-preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.preview-controls {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 8px 16px;
  border-radius: 24px;
  z-index: 2001;
}

.preview-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.preview-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

.preview-btn.close {
  margin-left: 8px;
  background: rgba(255, 107, 107, 0.3);
  border-color: rgba(255, 107, 107, 0.5);
}

.preview-btn.close:hover {
  background: rgba(255, 107, 107, 0.5);
}

.zoom-level {
  color: white;
  font-size: 14px;
  min-width: 40px;
  text-align: center;
}

.preview-image-container {
  overflow: hidden;
  width: 100%;
  height: 100%;
  position: relative;
}

.preview-image-container img {
  position: absolute;
  top: 50%;
  left: 50%;
  max-width: 85vw;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 8px;
  transition: transform 0.05s ease-out;
  will-change: transform;
}

/* 新消息提示按钮 */
.new-message-hint {
  position: absolute;
  bottom: 80px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #FF9EB5, #FFB8CC);
  color: white;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 6px 20px rgba(255, 158, 181, 0.45);
  z-index: 10;
  transition: all 0.2s ease;
}

.new-message-hint:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 158, 181, 0.55);
}

.arrow-icon {
  width: 18px;
  height: 18px;
  animation: bounceDown 1s infinite;
}

@keyframes bounceDown {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(3px); }
}

.message-count {
  background: white;
  color: #FF9EB5;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  min-width: 20px;
  text-align: center;
}

.hint-text {
  font-size: 14px;
}

/* 弹出动画 */
.bounce-enter-active {
  animation: bounceIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.bounce-leave-active {
  animation: bounceOut 0.2s ease-in;
}

@keyframes bounceIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.8);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes bounceOut {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(10px) scale(0.9);
  }
}
</style>
