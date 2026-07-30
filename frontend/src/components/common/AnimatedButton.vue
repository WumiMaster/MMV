<template>
  <!-- 带弹性动画的按钮 -->
  <button
    class="animated-btn"
    :class="[variant, size, { 'btn-loading': loading }]"
    :disabled="disabled || loading"
    @click="handleClick"
    @mousedown="isPressed = true"
    @mouseup="isPressed = false"
    @mouseleave="isPressed = false"
    @touchstart.passive="isPressed = true"
    @touchend="isPressed = false"
  >
    <!-- 加载动画 -->
    <span v-if="loading" class="btn-spinner"></span>

    <!-- 按钮内容 -->
    <span class="btn-content" :class="{ 'opacity-0': loading }">
      <slot></slot>
    </span>

    <!-- 点击波纹效果 -->
    <span
      v-for="ripple in ripples"
      :key="ripple.id"
      class="ripple"
      :style="ripple.style"
    ></span>
  </button>
</template>

<script setup>
/**
 * 带动画效果的按钮组件
 * 支持弹性缩放、点击波纹、加载状态
 */

import { ref } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (val) => ['primary', 'secondary', 'ghost', 'danger'].includes(val)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (val) => ['small', 'medium', 'large'].includes(val)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const isPressed = ref(false)
const ripples = ref([])
let rippleId = 0

// 处理点击
function handleClick(event) {
  if (props.disabled || props.loading) return

  // 创建波纹效果
  createRipple(event)

  // 触发点击事件
  emit('click', event)
}

// 创建波纹
function createRipple(event) {
  const button = event.currentTarget
  const rect = button.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height)
  const x = event.clientX - rect.left - size / 2
  const y = event.clientY - rect.top - size / 2

  const ripple = {
    id: rippleId++,
    style: {
      width: `${size}px`,
      height: `${size}px`,
      left: `${x}px`,
      top: `${y}px`
    }
  }

  ripples.value.push(ripple)

  // 动画结束后移除
  setTimeout(() => {
    ripples.value = ripples.value.filter(r => r.id !== ripple.id)
  }, 600)
}
</script>

<style scoped>
.animated-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 14px;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.animated-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.animated-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 尺寸变体 */
.animated-btn.small {
  height: 36px;
  padding: 0 16px;
  font-size: 13px;
  border-radius: 10px;
}

.animated-btn.medium {
  height: 48px;
  padding: 0 24px;
  font-size: 15px;
  border-radius: 14px;
}

.animated-btn.large {
  height: 56px;
  padding: 0 32px;
  font-size: 17px;
  border-radius: 16px;
}

/* 颜色变体 */
.animated-btn.primary {
  background: linear-gradient(135deg, #FF9EB5, #FFB8CC);
  color: white;
  box-shadow: 0 4px 16px rgba(255, 158, 181, 0.4);
}

.animated-btn.primary:hover:not(:disabled) {
  box-shadow: 0 6px 24px rgba(255, 158, 181, 0.5);
  background: linear-gradient(135deg, #FFB0C5, #FFC8D8);
}

.animated-btn.primary:active:not(:disabled) {
  box-shadow: 0 2px 8px rgba(255, 158, 181, 0.3);
}

.animated-btn.secondary {
  background: linear-gradient(135deg, #7ED7A7, #A0E8C0);
  color: white;
  box-shadow: 0 4px 16px rgba(126, 215, 167, 0.4);
}

.animated-btn.secondary:hover:not(:disabled) {
  box-shadow: 0 6px 24px rgba(126, 215, 167, 0.5);
  background: linear-gradient(135deg, #90E0B5, #B0F0C8);
}

.animated-btn.secondary:active:not(:disabled) {
  box-shadow: 0 2px 8px rgba(126, 215, 167, 0.3);
}

.animated-btn.ghost {
  background: rgba(255, 242, 248, 0.6);
  color: #666;
  border: 1px solid rgba(200, 190, 198, 0.5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.animated-btn.ghost:hover:not(:disabled) {
  background: rgba(255, 232, 242, 0.8);
  border-color: rgba(255, 180, 200, 0.6);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.animated-btn.danger {
  background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
  color: white;
  box-shadow: 0 4px 16px rgba(255, 107, 107, 0.4);
}

.animated-btn.danger:hover:not(:disabled) {
  box-shadow: 0 6px 24px rgba(255, 107, 107, 0.5);
  background: linear-gradient(135deg, #FF8080, #FFA0A0);
}

/* 加载状态 */
.btn-loading {
  pointer-events: none;
}

.btn-spinner {
  position: absolute;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s ease;
}

.opacity-0 {
  opacity: 0;
}

/* 波纹效果 */
.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  transform: scale(0);
  animation: ripple-animation 0.6s ease-out;
  pointer-events: none;
}

@keyframes ripple-animation {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
</style>
