<template>
  <!-- 网络监控组件 -->
  <div class="network-monitor" v-if="isVisible">
    <!-- 上行 -->
    <div class="stat-row">
      <div class="stat-label">
        <svg class="stat-icon upload" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="17 11 12 6 7 11"></polyline>
          <line x1="12" y1="6" x2="12" y2="18"></line>
        </svg>
        <span>上行</span>
      </div>
      <div class="stat-values">
        <span class="stat-current">{{ uploadSpeed }}</span>
        <span class="stat-avg">平均 {{ uploadAvg }}</span>
        <span class="stat-peak" @click.stop="resetUploadPeak" title="点击重置峰值">
          峰值 {{ uploadPeak }}
        </span>
      </div>
    </div>

    <!-- 下行 -->
    <div class="stat-row">
      <div class="stat-label">
        <svg class="stat-icon download" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="7 13 12 18 17 13"></polyline>
          <line x1="12" y1="18" x2="12" y2="6"></line>
        </svg>
        <span>下行</span>
      </div>
      <div class="stat-values">
        <span class="stat-current">{{ downloadSpeed }}</span>
        <span class="stat-avg">平均 {{ downloadAvg }}</span>
        <span class="stat-peak" @click.stop="resetDownloadPeak" title="点击重置峰值">
          峰值 {{ downloadPeak }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 网络监控组件
 * 显示实时速度、5秒平均值、峰值（可重置）
 */

import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(true)

// 实时速度
const uploadSpeed = ref('0 KB/s')
const downloadSpeed = ref('0 KB/s')

// 5秒平均
const uploadAvg = ref('0 KB/s')
const downloadAvg = ref('0 KB/s')

// 峰值
const uploadPeak = ref('0 KB/s')
const downloadPeak = ref('0 KB/s')

// 速度历史记录（用于计算平均）
const uploadHistory = ref([])
const downloadHistory = ref([])

let statsTimer = null
const HISTORY_LENGTH = 5 // 5秒历史

// 格式化速度
function formatSpeed(bytesPerSecond) {
  if (bytesPerSecond < 1024) return bytesPerSecond.toFixed(0) + ' B/s'
  if (bytesPerSecond < 1024 * 1024) return (bytesPerSecond / 1024).toFixed(1) + ' KB/s'
  return (bytesPerSecond / (1024 * 1024)).toFixed(1) + ' MB/s'
}

// 计算平均值
function calcAverage(history) {
  if (history.length === 0) return 0
  const sum = history.reduce((a, b) => a + b, 0)
  return sum / history.length
}

// 从全局状态获取速度
function updateSpeeds() {
  if (!window.__networkStats) return

  const upload = window.__networkStats.uploadSpeed || 0
  const download = window.__networkStats.downloadSpeed || 0

  // 更新实时速度
  uploadSpeed.value = formatSpeed(upload)
  downloadSpeed.value = formatSpeed(download)

  // 更新历史记录
  uploadHistory.value.push(upload)
  downloadHistory.value.push(download)

  // 保持历史记录长度
  if (uploadHistory.value.length > HISTORY_LENGTH) {
    uploadHistory.value.shift()
  }
  if (downloadHistory.value.length > HISTORY_LENGTH) {
    downloadHistory.value.shift()
  }

  // 计算平均值
  uploadAvg.value = formatSpeed(calcAverage(uploadHistory.value))
  downloadAvg.value = formatSpeed(calcAverage(downloadHistory.value))

  // 更新峰值
  const uploadPeakNum = parseFloat(uploadPeak.value) || 0
  const downloadPeakNum = parseFloat(downloadPeak.value) || 0

  const uploadSpeedNum = parseFloat(formatSpeed(upload)) || 0
  const downloadSpeedNum = parseFloat(formatSpeed(download)) || 0

  if (uploadSpeedNum > uploadPeakNum) {
    uploadPeak.value = formatSpeed(upload)
  }
  if (downloadSpeedNum > downloadPeakNum) {
    downloadPeak.value = formatSpeed(download)
  }
}

// 重置峰值
function resetUploadPeak() {
  uploadPeak.value = '0 KB/s'
}

function resetDownloadPeak() {
  downloadPeak.value = '0 KB/s'
}

// 开始监控
function startMonitoring() {
  if (statsTimer) {
    clearInterval(statsTimer)
  }
  statsTimer = setInterval(updateSpeeds, 1000)
}

// 停止监控
function stopMonitoring() {
  if (statsTimer) {
    clearInterval(statsTimer)
    statsTimer = null
  }
}

onMounted(() => {
  startMonitoring()
})

onUnmounted(() => {
  stopMonitoring()
})

defineExpose({
  startMonitoring,
  stopMonitoring
})
</script>

<style scoped>
.network-monitor {
  background: rgba(255, 240, 248, 0.5);
  border: 1px solid rgba(220, 210, 218, 0.3);
  border-radius: 10px;
  padding: 8px 10px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-sizing: border-box;
  overflow: hidden;
}

.stat-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.stat-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #888;
  min-width: 40px;
}

.stat-icon {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
}

.stat-icon.upload {
  color: #FF7A9E;
}

.stat-icon.download {
  color: #5CB87A;
}

.stat-values {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-family: monospace;
  flex: 1;
  justify-content: flex-end;
}

.stat-current {
  color: #555;
  font-weight: 600;
  text-align: right;
}

.stat-avg {
  color: #888;
  text-align: right;
}

.stat-peak {
  color: #e0557a;
  text-align: right;
  cursor: pointer;
  padding: 1px 3px;
  border-radius: 3px;
  transition: background 0.2s ease;
}

.stat-peak:hover {
  background: rgba(255, 158, 181, 0.15);
}
</style>
