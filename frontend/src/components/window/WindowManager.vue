<template>
  <!-- 窗口管理器 -->
  <div class="window-manager">
    <!-- 文字频道窗口（上方） -->
    <div v-if="textWindow" class="window-panel text-panel">
      <ChatWindow
        :sub-channel-id="textWindow.subChannelId"
        :sub-channel-name="textWindow.title"
        :current-user-id="currentUserId"
        @send="handleSendMessage"
      />
    </div>

    <!-- 语音频道窗口（下方） -->
    <div v-if="voiceWindow" class="window-panel voice-panel">
      <VoiceWindow
        ref="voiceWindowRef"
        :sub-channel-id="voiceWindow.subChannelId"
        :sub-channel-name="voiceWindow.title"
        :channel-id="voiceWindow.channelId"
        @close="closeVoiceWindow"
      />
      <AudioLevelIndicator
        :show="true"
        :stream="voiceStream"
      />
    </div>

    <!-- 空状态 -->
    <div v-if="!textWindow && !voiceWindow" class="empty-state">
      <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
      <div class="empty-title">选择一个子频道开始聊天</div>
      <div class="empty-desc">从左侧选择文字或语音子频道</div>
    </div>
  </div>
</template>

<script setup>
/**
 * 窗口管理器组件
 * 管理文字和语音窗口的显示
 * 一次只显示一个文字频道和一个语音频道
 */

import { ref, nextTick } from 'vue'
import ChatWindow from '../channel/ChatWindow.vue'
import VoiceWindow from '../channel/VoiceWindow.vue'
import AudioLevelIndicator from '../common/AudioLevelIndicator.vue'

const props = defineProps({
  currentUserId: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['send-message'])

// 文字窗口状态
const textWindow = ref(null)

// 语音窗口状态
const voiceWindow = ref(null)
const voiceWindowRef = ref(null)
const voiceStream = ref(null)

// 打开文字窗口
function openTextWindow(config) {
  textWindow.value = {
    subChannelId: config.subChannelId,
    title: config.title
  }
}

// 打开语音窗口
function openVoiceWindow(config) {
  voiceWindow.value = {
    subChannelId: config.subChannelId,
    channelId: config.channelId,
    title: config.title
  }
  // 延迟获取语音流
  nextTick(() => {
    setTimeout(updateVoiceStream, 1000)
  })
}

// 关闭文字窗口
function closeTextWindow() {
  textWindow.value = null
}

// 关闭语音窗口
function closeVoiceWindow() {
  voiceStream.value = null
  voiceWindow.value = null
}

// 获取语音流
function updateVoiceStream() {
  if (voiceWindowRef.value && voiceWindowRef.value.localStream) {
    voiceStream.value = voiceWindowRef.value.localStream
  }
}

// 发送消息
function handleSendMessage(message) {
  emit('send-message', message)
}

// 检查窗口是否打开
function isTextWindowOpen(subChannelId) {
  return textWindow.value?.subChannelId === subChannelId
}

function isVoiceWindowOpen(subChannelId) {
  return voiceWindow.value?.subChannelId === subChannelId
}

// 添加消息到文字窗口
function addMessage(message) {
  // 如果消息属于当前打开的文字窗口，需要通过 ChatWindow 的 ref 添加
  // 这里我们通过事件通知 ChannelPage，由 ChannelPage 处理
}

// 暴露方法
defineExpose({
  openTextWindow,
  openVoiceWindow,
  closeTextWindow,
  closeVoiceWindow,
  isTextWindowOpen,
  isVoiceWindowOpen,
  getTextWindowSubChannelId: () => textWindow.value?.subChannelId
})
</script>

<style scoped>
.window-manager {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 1px;
  background: rgba(220, 210, 218, 0.3);
}

/* 窗口面板 */
.window-panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: rgba(255, 245, 250, 0.4);
  animation: panelSlideIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* 文字频道窗口占更多空间 */
.text-panel {
  flex: 1;
}

/* 语音频道窗口 - 足够显示用户列表 */
.voice-panel {
  flex: 0 0 280px;
}

@keyframes panelSlideIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #888;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 20px;
  color: #ccc;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: #555;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: #999;
}
</style>
