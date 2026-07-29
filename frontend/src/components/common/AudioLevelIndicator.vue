<template>
  <!-- 音频电平指示器 -->
  <div class="audio-level-indicator" v-if="isVisible">
    <div class="indicator-label">
      <svg class="mic-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="23"></line>
        <line x1="8" y1="23" x2="16" y2="23"></line>
      </svg>
      <span>麦克风</span>
    </div>
    <div class="level-bar-container">
      <div
        class="level-bar"
        :style="{ width: levelPercent + '%' }"
        :class="{ active: level > 30, high: level > 70 }"
      ></div>
    </div>
    <span class="level-value">{{ Math.round(level) }}%</span>
  </div>
</template>

<script setup>
/**
 * 音频电平指示器组件
 * 显示麦克风输入音量级别
 */

import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  // 是否显示
  show: {
    type: Boolean,
    default: false
  },
  // 音频流（MediaStream）
  stream: {
    type: MediaStream,
    default: null
  }
})

const isVisible = ref(false)
const level = ref(0)
const levelPercent = ref(0)

let audioContext = null
let analyser = null
let animationFrame = null

// 开始监听音频流
function startMonitoring(stream) {
  if (!stream) return

  try {
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    const source = audioContext.createMediaStreamSource(stream)
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 256
    analyser.smoothingTimeConstant = 0.8
    source.connect(analyser)

    updateLevel()
  } catch (e) {
    console.error('音频监控启动失败:', e)
  }
}

// 停止监听
function stopMonitoring() {
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
    animationFrame = null
  }
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }
  analyser = null
  level.value = 0
  levelPercent.value = 0
}

// 更新音量级别
function updateLevel() {
  if (!analyser) return

  const dataArray = new Uint8Array(analyser.frequencyBinCount)
  analyser.getByteFrequencyData(dataArray)

  // 计算平均音量
  const sum = dataArray.reduce((acc, val) => acc + val, 0)
  const avg = sum / dataArray.length

  // 转换为百分比 (0-100)
  level.value = Math.min(100, avg * 100 / 128)
  levelPercent.value = level.value

  animationFrame = requestAnimationFrame(updateLevel)
}

// 监听 show 属性变化
watch(() => props.show, (newVal) => {
  isVisible.value = newVal
  if (!newVal) {
    stopMonitoring()
  }
})

// 监听 stream 属性变化
watch(() => props.stream, (newStream) => {
  if (newStream && props.show) {
    startMonitoring(newStream)
  } else {
    stopMonitoring()
  }
})

onMounted(() => {
  isVisible.value = props.show
  if (props.stream && props.show) {
    startMonitoring(props.stream)
  }
})

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
.audio-level-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: rgba(255, 240, 248, 0.6);
  border-top: 1px solid rgba(255, 220, 230, 0.4);
  font-size: 12px;
}

.indicator-label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  min-width: 70px;
}

.mic-icon {
  width: 14px;
  height: 14px;
  color: #888;
}

.level-bar-container {
  flex: 1;
  height: 6px;
  background: rgba(200, 190, 198, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.level-bar {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, #7ED7A7, #A0E8C0);
  border-radius: 3px;
  transition: width 0.1s ease;
}

.level-bar.active {
  background: linear-gradient(90deg, #7ED7A7, #FFD700);
}

.level-bar.high {
  background: linear-gradient(90deg, #FFD700, #FF6B6B);
}

.level-value {
  color: #888;
  min-width: 35px;
  text-align: right;
  font-family: monospace;
}
</style>
