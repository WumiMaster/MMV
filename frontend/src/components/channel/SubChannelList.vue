<template>
  <!-- 子频道列表 -->
  <div class="sub-channel-list">
    <div class="sub-channel-header">
      <div class="channel-title">{{ channelName }}</div>
      <div class="channel-id" @click="copyChannelId">
        ID: {{ channelId }}
        <svg class="copy-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
      </div>
    </div>

    <div class="sub-channel-sections">
      <!-- 文字子频道 -->
      <div class="section">
        <div class="section-title">文字频道</div>
        <div
          v-for="sc in textChannels"
          :key="sc.id"
          class="sub-channel-item"
          :class="{ active: currentSubChannel?.id === sc.id }"
          @click="$emit('select-sub-channel', sc)"
        >
          <span class="icon">#</span>
          <span class="name">{{ sc.name }}</span>
        </div>
        <div v-if="textChannels.length === 0" class="empty-tip">
          暂无文字频道
        </div>
      </div>

      <!-- 语音子频道 -->
      <div class="section">
        <div class="section-title">语音频道</div>
        <div
          v-for="sc in voiceChannels"
          :key="sc.id"
          class="sub-channel-item voice"
          :class="{ active: currentSubChannel?.id === sc.id }"
          @click="$emit('select-sub-channel', sc)"
        >
          <svg class="icon voice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
          <span class="name">{{ sc.name }}</span>
        </div>
        <div v-if="voiceChannels.length === 0" class="empty-tip">
          暂无语音频道
        </div>
      </div>
    </div>

    <!-- Toast 提示 -->
    <div v-if="showToast" class="toast" :class="{ show: showToast }">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
/**
 * 子频道列表组件
 * 显示频道下的文字和语音子频道
 */

import { computed, ref } from 'vue'

const props = defineProps({
  channelName: {
    type: String,
    default: ''
  },
  channelId: {
    type: String,
    default: ''
  },
  subChannels: {
    type: Array,
    default: () => []
  },
  currentSubChannel: {
    type: Object,
    default: null
  }
})

defineEmits(['select-sub-channel'])

// 分类子频道
const textChannels = computed(() => props.subChannels.filter(sc => sc.type === 'text'))
const voiceChannels = computed(() => props.subChannels.filter(sc => sc.type === 'voice'))

// Toast 提示
const showToast = ref(false)
const toastMessage = ref('')

function showToastMsg(msg) {
  toastMessage.value = msg
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 2000)
}

// 复制频道ID
function copyChannelId() {
  navigator.clipboard.writeText(props.channelId).then(() => {
    showToastMsg('已复制频道ID')
  }).catch(() => {
    showToastMsg('复制失败')
  })
}
</script>

<style scoped>
.sub-channel-list {
  width: 100%;
  background: linear-gradient(
    180deg,
    rgba(255, 238, 248, 0.55) 0%,
    rgba(255, 242, 248, 0.45) 100%
  );
  -webkit-backdrop-filter: blur(20px);
  backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.sub-channel-header {
  padding: 16px;
  border-bottom: 1px solid rgba(220, 200, 210, 0.45);
}

.channel-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.channel-id {
  font-size: 12px;
  color: #999;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.channel-id:hover {
  color: #666;
}

.copy-icon-svg {
  width: 12px;
  height: 12px;
  vertical-align: middle;
}

.sub-channel-sections {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 12px;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
  padding: 4px 8px;
  margin-bottom: 4px;
}

.sub-channel-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  margin-bottom: 3px;
  border: 1px solid rgba(200, 190, 195, 0.45);
  background: rgba(255, 245, 250, 0.4);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  will-change: background, border-color, box-shadow;
}

.sub-channel-item:hover {
  background: rgba(255, 218, 232, 0.55);
  border-color: rgba(255, 200, 218, 0.6);
  box-shadow: 0 3px 8px rgba(255, 158, 181, 0.12);
}

.sub-channel-item.active {
  background: linear-gradient(135deg, rgba(255, 188, 212, 0.6), rgba(255, 202, 222, 0.5));
  box-shadow: 0 3px 12px rgba(255, 158, 181, 0.2);
  border-color: rgba(255, 168, 192, 0.65);
}

.sub-channel-item .icon {
  font-size: 16px;
  color: #888;
}

.voice-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.sub-channel-item .name {
  font-size: 14px;
  font-weight: 500;
  color: #444;
}

.empty-tip {
  padding: 8px;
  color: #999;
  font-size: 12px;
}

/* Toast 提示 */
.toast {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  opacity: 0;
  transition: all 0.3s;
  pointer-events: none;
}

.toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
</style>
