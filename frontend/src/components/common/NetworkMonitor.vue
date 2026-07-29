<template>
  <!-- 网络监控组件 -->
  <div class="network-monitor" v-if="isVisible">
    <div class="network-stats">
      <div class="stat-item upload">
        <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="17 11 12 6 7 11"></polyline>
          <line x1="12" y1="6" x2="12" y2="18"></line>
        </svg>
        <span class="stat-value">{{ uploadSpeed }}</span>
      </div>
      <div class="stat-item download">
        <svg class="stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="7 13 12 18 17 13"></polyline>
          <line x1="12" y1="18" x2="12" y2="6"></line>
        </svg>
        <span class="stat-value">{{ downloadSpeed }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 网络监控组件
 * 使用全局状态来监控网络速度
 */

import { ref, onMounted, onUnmounted, watch } from 'vue'

const isVisible = ref(true)
const uploadSpeed = ref('0 KB/s')
const downloadSpeed = ref('0 KB/s')

let statsTimer = null

// 格式化速度
function formatSpeed(bytesPerSecond) {
  if (bytesPerSecond < 1024) return bytesPerSecond.toFixed(0) + ' B/s'
  if (bytesPerSecond < 1024 * 1024) return (bytesPerSecond / 1024).toFixed(1) + ' KB/s'
  return (bytesPerSecond / (1024 * 1024)).toFixed(1) + ' MB/s'
}

// 从全局状态获取速度
function updateSpeeds() {
  if (window.__networkStats) {
    uploadSpeed.value = formatSpeed(window.__networkStats.uploadSpeed || 0)
    downloadSpeed.value = formatSpeed(window.__networkStats.downloadSpeed || 0)
  }
}

// 开始监控
function startMonitoring() {
  if (statsTimer) {
    clearInterval(statsTimer)
  }
  // 每秒更新一次
  statsTimer = setInterval(updateSpeeds, 1000)
}

// 停止监控
function stopMonitoring() {
  if (statsTimer) {
    clearInterval(statsTimer)
    statsTimer = null
  }
}

// 组件挂载时开始监控
onMounted(() => {
  startMonitoring()
})

// 组件卸载时停止监控
onUnmounted(() => {
  stopMonitoring()
})

// 暴露方法给父组件
defineExpose({
  startMonitoring,
  stopMonitoring
})
</script>

<style scoped>
.network-monitor {
  position: fixed;
  bottom: 16px;
  left: 16px;
  z-index: 100;
  background: linear-gradient(135deg, rgba(255, 240, 248, 0.75), rgba(240, 255, 245, 0.7));
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  padding: 8px 12px;
  min-width: 120px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.network-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-family: monospace;
}

.stat-icon {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.upload .stat-icon {
  color: #FF7A9E;
}

.upload .stat-value {
  color: #e0557a;
  font-weight: 500;
}

.download .stat-icon {
  color: #5CB87A;
}

.download .stat-value {
  color: #3a9d5c;
  font-weight: 500;
}
</style>
