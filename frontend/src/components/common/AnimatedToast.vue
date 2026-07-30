<template>
  <!-- 带动画的通知提示 -->
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast-item"
        :class="[toast.type, { 'toast-entering': toast.entering }]"
        @click="removeToast(toast.id)"
      >
        <!-- 图标 -->
        <span class="toast-icon">
          <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <svg v-else-if="toast.type === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          <svg v-else-if="toast.type === 'warning'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
            <line x1="12" y1="9" x2="12" y2="13"></line>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </span>

        <!-- 消息内容 -->
        <span class="toast-message">{{ toast.message }}</span>

        <!-- 关闭按钮 -->
        <button class="toast-close" @click.stop="removeToast(toast.id)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <!-- 进度条 -->
        <div class="toast-progress" :style="{ animationDuration: toast.duration + 'ms' }"></div>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
/**
 * 带动画效果的通知组件
 * 支持多种类型、自动消失、堆叠显示
 */

import { ref, onUnmounted } from 'vue'

const toasts = ref([])
let toastId = 0
const timers = new Map()

// 显示通知
function show(message, type = 'info', duration = 3000) {
  const id = toastId++
  const toast = {
    id,
    message,
    type,
    duration,
    entering: true
  }

  toasts.value.push(toast)

  // 移除进入动画标记
  setTimeout(() => {
    const t = toasts.value.find(t => t.id === id)
    if (t) t.entering = false
  }, 300)

  // 自动移除
  if (duration > 0) {
    const timer = setTimeout(() => {
      removeToast(id)
    }, duration)
    timers.set(id, timer)
  }

  return id
}

// 移除通知
function removeToast(id) {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }

  // 清除定时器
  if (timers.has(id)) {
    clearTimeout(timers.get(id))
    timers.delete(id)
  }
}

// 快捷方法
function success(message, duration) {
  return show(message, 'success', duration)
}

function error(message, duration) {
  return show(message, 'error', duration)
}

function warning(message, duration) {
  return show(message, 'warning', duration)
}

function info(message, duration) {
  return show(message, 'info', duration)
}

// 组件卸载时清理
onUnmounted(() => {
  timers.forEach(timer => clearTimeout(timer))
  timers.clear()
})

// 暴露方法
defineExpose({
  show,
  success,
  error,
  warning,
  info,
  removeToast
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
}

.toast-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.8);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.toast-item:hover {
  transform: translateX(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 类型样式 */
.toast-item.success {
  border-left: 4px solid #51CF66;
}

.toast-item.success .toast-icon {
  color: #51CF66;
}

.toast-item.error {
  border-left: 4px solid #FF6B6B;
}

.toast-item.error .toast-icon {
  color: #FF6B6B;
}

.toast-item.warning {
  border-left: 4px solid #FFD43B;
}

.toast-item.warning .toast-icon {
  color: #FFD43B;
}

.toast-item.info {
  border-left: 4px solid #74C0FC;
}

.toast-item.info .toast-icon {
  color: #74C0FC;
}

/* 图标 */
.toast-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast-icon svg {
  width: 100%;
  height: 100%;
}

/* 消息 */
.toast-message {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  line-height: 1.4;
}

/* 关闭按钮 */
.toast-close {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  flex-shrink: 0;
}

.toast-item:hover .toast-close {
  opacity: 1;
}

.toast-close svg {
  width: 16px;
  height: 16px;
  color: #999;
}

.toast-close:hover svg {
  color: #666;
}

/* 进度条 */
.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #FF9EB5, #7ED7A7);
  animation: progress linear forwards;
}

@keyframes progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

/* 进入/离开动画 */
.toast-enter-active {
  animation: toastIn 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.toast-leave-active {
  animation: toastOut 0.3s ease-in forwards;
}

.toast-move {
  transition: transform 0.3s ease;
}

@keyframes toastIn {
  from {
    opacity: 0;
    transform: translateX(100px) scale(0.8);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes toastOut {
  from {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateX(100px) scale(0.8);
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .toast-container {
    right: 10px;
    left: 10px;
    max-width: none;
  }
}
</style>
