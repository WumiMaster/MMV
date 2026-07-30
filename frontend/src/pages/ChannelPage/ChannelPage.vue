<template>
  <div class="channel-container">
    <!-- 顶部导航栏 -->
    <nav class="top-navbar">
      <!-- 移动端：子频道切换按钮 -->
      <button class="sidebar-toggle" @click="showSidebar = !showSidebar" v-if="currentChannel">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>

      <!-- 频道列表（水平滚动） -->
      <div class="nav-channels">
        <div
          v-for="channel in myChannels"
          :key="channel.id"
          class="nav-channel-item"
          :class="{ active: currentChannel?.id === channel.id }"
          @click="selectChannel(channel)"
        >
          <div class="channel-icon">
            <img v-if="channel.avatar" :src="channel.avatar + '?t=' + Date.now()" alt="频道头像" class="channel-avatar-img" />
            <span v-else>{{ channel.name.charAt(0) }}</span>
          </div>
          <span class="channel-name">{{ channel.name }}</span>
        </div>
        <button class="join-channel-btn" @click="showJoinModal = true" title="加入频道">
          <svg class="plus-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
      </div>

      <!-- 右侧：操作按钮 -->
      <div class="nav-right">
        <button class="icon-btn" title="设置" @click="openSettings">
          <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </button>
        <button class="icon-btn" title="退出登录" @click="handleLogout">
          <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 侧边栏遮罩（移动端） -->
      <div v-if="showSidebar" class="sidebar-overlay" @click="showSidebar = false"></div>

      <!-- 左侧：子频道列表 -->
      <div class="sidebar" :class="{ open: showSidebar }">
        <SubChannelList
          v-if="currentChannel"
          :channel-name="currentChannel.name"
          :channel-id="currentChannel.channel_id"
          :sub-channels="subChannels"
          :current-sub-channel="currentSubChannel"
          @select-sub-channel="handleSelectSubChannel"
        />
        <!-- 网络监控 -->
        <div class="sidebar-footer">
          <NetworkMonitor />
        </div>
      </div>

      <!-- 右侧：窗口区域 -->
      <div class="content-area">
        <!-- 频道信息栏（移动端隐藏） -->
        <div v-if="currentChannel" class="channel-info-bar">
          <span class="info-name">{{ currentChannel.name }}</span>
          <span class="info-id" @click="copyChannelId" title="点击复制">
            ID: {{ currentChannel.channel_id }}
            <svg class="copy-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
          </span>
        </div>

        <!-- 悬浮窗口管理器 -->
        <WindowManager
          ref="windowManagerRef"
          :current-user-id="authStore.user?.id"
          @send-message="handleSendMessage"
        />
      </div>
    </div>

    <!-- 加入频道弹窗 -->
    <JoinChannelModal
      v-if="showJoinModal"
      @close="showJoinModal = false"
      @joined="handleChannelJoined"
    />

    <!-- 设置弹窗 -->
    <SettingsWindow
      v-if="showSettings"
      @close="showSettings = false"
    />

    <!-- Toast 提示 -->
    <div v-if="showToast" class="toast" :class="{ show: showToast }">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
/**
 * 频道页面
 * 顶部导航栏显示频道列表，下方左侧显示子频道列表，右侧显示聊天窗口
 */

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'
import SubChannelList from '../../components/channel/SubChannelList.vue'
import WindowManager from '../../components/window/WindowManager.vue'
import JoinChannelModal from '../../components/channel/JoinChannelModal.vue'
import SettingsWindow from '../../components/channel/SettingsWindow.vue'
import NetworkMonitor from '../../components/common/NetworkMonitor.vue'

const router = useRouter()
const authStore = useAuthStore()

// 频道数据
const myChannels = ref([])
const currentChannel = ref(null)
const subChannels = ref([])
const currentSubChannel = ref(null)
const windowManagerRef = ref(null)

// UI 状态
const showSidebar = ref(false)
const showJoinModal = ref(false)
const showSettings = ref(false)
const showToast = ref(false)
const toastMessage = ref('')

// WebSocket 连接
let ws = null
let reconnectTimer = null
let reconnectAttempts = 0
const MAX_RECONNECT_ATTEMPTS = 5

// 显示提示
function showToastMsg(msg) {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 2000)
}

// 复制频道ID
function copyChannelId() {
  if (currentChannel.value) {
    navigator.clipboard.writeText(currentChannel.value.channel_id).then(() => {
      showToastMsg('已复制频道ID')
    }).catch(() => {
      showToastMsg('复制失败')
    })
  }
}

// 加载我的频道列表
async function loadMyChannels() {
  try {
    const response = await api.get('/api/channels/my')
    myChannels.value = response.data
  } catch (error) {
    console.error('加载频道列表失败:', error)
  }
}

// 选择频道
async function selectChannel(channel) {
  currentChannel.value = channel
  currentSubChannel.value = null

  // 关闭所有已打开的窗口
  if (windowManagerRef.value) {
    windowManagerRef.value.closeTextWindow()
    windowManagerRef.value.closeVoiceWindow()
  }

  // 加载子频道列表
  try {
    const response = await api.get(`/api/channels/${channel.id}`)
    subChannels.value = response.data.sub_channels

    // 自动打开第一个文字子频道
    const firstTextChannel = subChannels.value.find(sc => sc.type === 'text')
    if (firstTextChannel) {
      selectSubChannel(firstTextChannel)
    }
  } catch (error) {
    console.error('加载子频道失败:', error)
    subChannels.value = []
  }

  // 连接 WebSocket
  connectWebSocket(channel.id)
}

// 选择子频道（打开对应类型窗口）
function selectSubChannel(subChannel) {
  if (!windowManagerRef.value) return

  const config = {
    subChannelId: subChannel.id,
    channelId: currentChannel.value?.id,
    title: subChannel.name
  }

  if (subChannel.type === 'text') {
    windowManagerRef.value.openTextWindow(config)
  } else if (subChannel.type === 'voice') {
    windowManagerRef.value.openVoiceWindow(config)
  }

  currentSubChannel.value = subChannel
}

// 选择子频道并关闭侧边栏（移动端）
function handleSelectSubChannel(subChannel) {
  selectSubChannel(subChannel)
  // 移动端选择后关闭侧边栏
  if (window.innerWidth < 768) {
    showSidebar.value = false
  }
}

// 加入频道成功
function handleChannelJoined(channel) {
  showJoinModal.value = false
  loadMyChannels()
  selectChannel(channel)
}

// 发送消息后（用于 WebSocket 广播）
function handleSendMessage(message) {
  // 目前后端在保存消息时会自动广播
}

// 连接 WebSocket
function connectWebSocket(channelId) {
  // 断开现有连接
  if (ws) {
    ws.close()
  }

  const token = authStore.token
  if (!token) return

  // 创建 WebSocket 连接（通过 Vite 代理）
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = window.location.host // 包含端口
  const wsUrl = `${protocol}//${host}/ws/${channelId}?token=${token}`
  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket 连接成功')
    reconnectAttempts = 0 // 连接成功，重置重连次数
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      handleWebSocketMessage(data)
    } catch (e) {
      console.error('解析 WebSocket 消息失败:', e)
    }
  }

  ws.onclose = () => {
    console.log('WebSocket 连接关闭')
    // 尝试重连
    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
      reconnectAttempts++
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000) // 指数退避，最大30秒
      console.log(`${delay / 1000}秒后尝试第${reconnectAttempts}次重连...`)
      reconnectTimer = setTimeout(() => {
        if (currentChannel.value) {
          connectWebSocket(currentChannel.value.id)
        }
      }, delay)
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket 错误:', error)
  }
}

// 处理 WebSocket 消息
function handleWebSocketMessage(data) {
  switch (data.type) {
    case 'new_message':
      // 新消息：通过全局事件总线通知 ChatWindow
      if (data.message) {
        window.dispatchEvent(new CustomEvent('new-message', { detail: data.message }))
      }
      break
    // 不再显示加入/离开提示
    default:
      break
  }
}

// 打开设置
function openSettings() {
  showSettings.value = true
}

// 退出登录
function handleLogout() {
  // 清除重连定时器
  if (reconnectTimer) {
    clearTimeout(reconnectTimer)
    reconnectTimer = null
  }
  // 关闭 WebSocket
  if (ws) {
    ws.close()
    ws = null
  }
  authStore.logout()
  router.push('/login')
}

// 页面加载时获取频道列表
onMounted(() => {
  loadMyChannels()
})
</script>

<style scoped>
.channel-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

/* 顶部导航栏 - iOS 26 液态玻璃 */
.top-navbar {
  height: 64px;
  flex-shrink: 0;
  background: linear-gradient(
    90deg,
    rgba(255, 230, 240, 0.65) 0%,
    rgba(255, 240, 245, 0.55) 50%,
    rgba(230, 255, 240, 0.5) 100%
  );
  -webkit-backdrop-filter: blur(30px) saturate(150%);
  backdrop-filter: blur(30px) saturate(150%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

/* 导航栏左侧：频道列表 */
.nav-channels {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  overflow-x: auto;
  padding: 4px 0;
}

.nav-channels::-webkit-scrollbar {
  height: 4px;
}

.nav-channels::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
}

.nav-channel-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  white-space: nowrap;
  background: rgba(255, 242, 248, 0.6);
  border: 1px solid rgba(200, 190, 198, 0.5);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.07);
  flex-shrink: 0;
  will-change: background, border-color, box-shadow;
}

.nav-channel-item:hover {
  background: rgba(255, 218, 232, 0.72);
  box-shadow: 0 3px 12px rgba(255, 158, 181, 0.2);
  border-color: rgba(255, 195, 215, 0.72);
}

.nav-channel-item.active {
  background: linear-gradient(135deg, rgba(255, 168, 192, 0.65), rgba(255, 188, 208, 0.55));
  border-color: rgba(255, 148, 178, 0.72);
  box-shadow: 0 3px 14px rgba(255, 158, 181, 0.28);
}

.nav-channel-item .channel-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
  overflow: hidden;
}

.channel-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.nav-channel-item .channel-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.join-channel-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px dashed rgba(126, 215, 167, 0.75);
  background: rgba(126, 215, 167, 0.25);
  color: #2b8a3e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
  flex-shrink: 0;
  padding: 0;
  box-shadow: 0 3px 10px rgba(126, 215, 167, 0.2);
}

.plus-svg {
  width: 18px;
  height: 18px;
}

.join-channel-btn:hover {
  background: rgba(126, 215, 167, 0.35);
  border-color: #7ED7A7;
  box-shadow: 0 4px 12px rgba(126, 215, 167, 0.25);
}

/* 导航栏右侧 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  margin-left: 16px;
}

.current-channel-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(255, 242, 248, 0.6);
  border: 1px solid rgba(200, 190, 198, 0.5);
  border-radius: 14px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.info-name {
  font-weight: 600;
  font-size: 14px;
  color: #333;
}

.info-id {
  font-size: 12px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: rgba(255, 242, 248, 0.55);
  border: 1px solid rgba(200, 190, 198, 0.45);
  border-radius: 6px;
  transition: background 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.info-id:hover {
  background: rgba(255, 232, 242, 0.65);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.copy-icon-svg {
  width: 12px;
  height: 12px;
  vertical-align: middle;
}

.icon-svg {
  width: 20px;
  height: 20px;
}

.no-channel-tip {
  color: #999;
  font-size: 14px;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid rgba(200, 190, 198, 0.5);
  background: rgba(255, 238, 245, 0.6);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  font-size: 18px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  will-change: background, box-shadow;
}

.icon-btn:hover {
  background: rgba(255, 215, 228, 0.72);
  border-color: rgba(255, 185, 205, 0.65);
  box-shadow: 0 3px 12px rgba(255, 158, 181, 0.22);
}

/* 侧边栏切换按钮 */
.sidebar-toggle {
  display: flex;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: none;
  background: rgba(255, 238, 245, 0.6);
  cursor: pointer;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sidebar-toggle svg {
  width: 20px;
  height: 20px;
  color: #666;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
  min-height: 0;
  position: relative;
}

/* 侧边栏（抽屉式） */
.sidebar {
  position: fixed;
  top: 64px;
  left: 0;
  bottom: 0;
  width: 280px;
  z-index: 200;
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 245, 250, 0.95);
  -webkit-backdrop-filter: blur(20px);
  backdrop-filter: blur(20px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* 阴影层（独立元素，平滑过渡） */
.sidebar::after {
  content: '';
  position: absolute;
  top: 0;
  right: -20px;
  bottom: 0;
  width: 20px;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.08), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.sidebar.open::after {
  opacity: 1;
}

.sidebar.open {
  transform: translateX(0);
}

/* 侧边栏遮罩 */
.sidebar-overlay {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 199;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 频道信息栏 */
.channel-info-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: rgba(255, 242, 248, 0.4);
  border-bottom: 1px solid rgba(220, 210, 218, 0.3);
  flex-shrink: 0;
}

.info-name {
  font-weight: 600;
  font-size: 14px;
  color: #333;
}

.info-id {
  font-size: 12px;
  color: #888;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: rgba(255, 240, 248, 0.5);
  border: 1px solid rgba(220, 210, 218, 0.4);
  border-radius: 6px;
  transition: background 0.2s ease;
}

.info-id:hover {
  background: rgba(255, 232, 242, 0.6);
}

.copy-icon-svg {
  width: 12px;
  height: 12px;
}

.content-area {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: linear-gradient(
    135deg,
    rgba(255, 245, 250, 0.3) 0%,
    rgba(250, 240, 255, 0.2) 50%,
    rgba(240, 255, 245, 0.25) 100%
  );
}

/* 空状态 */
.empty-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #555;
  pointer-events: none;
}

.empty-icon-svg {
  width: 64px;
  height: 64px;
  margin-bottom: 20px;
  color: #bbb;
}

.empty-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #444;
}

.empty-desc {
  color: #888;
  font-size: 14px;
  text-align: center;
}

/* 语音频道占位 */
.voice-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  height: 100%;
}

.voice-icon-svg {
  width: 64px;
  height: 64px;
  margin-bottom: 20px;
  color: #999;
}

.voice-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #444;
}

.voice-desc {
  color: #888;
  font-size: 14px;
}

/* Toast 提示 */
.toast {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%) translateY(-20px);
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  padding: 14px 24px;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s;
  z-index: 2000;
}

.toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* 内容区域动画 - iOS 风格 */
.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.voice-content-wrapper {
  display: flex;
  flex-direction: column;
}

.voice-content-wrapper > :first-child {
  flex: 1;
  min-height: 0;
}

.animate-in {
  animation: contentSlideIn 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes contentSlideIn {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 频道名称在侧边栏模式下隐藏 */
.nav-channel-item .channel-name {
  display: none;
}

/* 频道信息栏隐藏（信息已在侧边栏显示） */
.channel-info-bar {
  display: none;
}

/* 侧边栏底部 */
.sidebar-footer {
  flex-shrink: 0;
  padding: 12px;
  border-top: 1px solid rgba(220, 210, 218, 0.3);
  background: rgba(255, 245, 250, 0.6);
}
</style>
