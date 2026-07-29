<template>
  <!-- 悬浮窗口 -->
  <div
    class="floating-window"
    :class="{ minimized: isMinimized, active: isActive }"
    :style="windowStyle"
    @mousedown="$emit('focus')"
  >
    <!-- 窗口头部 -->
    <div
      class="window-header"
      @mousedown.start="startDrag"
    >
      <div class="window-title">
        <span class="window-icon">
          <svg v-if="type === 'text'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          </svg>
        </span>
        <span class="window-name">{{ title }}</span>
      </div>
      <div class="window-actions">
        <button class="action-btn minimize" @click.stop="$emit('minimize')" title="最小化">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
        <button class="action-btn close" @click.stop="$emit('close')" title="关闭">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- 窗口内容 -->
    <div class="window-content" v-show="!isMinimized">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
/**
 * 悬浮窗口组件
 * 支持拖拽、最小化、关闭、层级管理
 */

import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  },
  title: {
    type: String,
    default: '窗口'
  },
  type: {
    type: String,
    default: 'text',
    validator: (val) => ['text', 'voice'].includes(val)
  },
  isActive: {
    type: Boolean,
    default: false
  },
  zIndex: {
    type: Number,
    default: 10
  },
  initialX: {
    type: Number,
    default: 100
  },
  initialY: {
    type: Number,
    default: 100
  },
  width: {
    type: Number,
    default: 600
  },
  height: {
    type: Number,
    default: 450
  }
})

const emit = defineEmits(['focus', 'minimize', 'close', 'move'])

// 窗口状态
const position = ref({ x: props.initialX, y: props.initialY })
const size = ref({ width: props.width, height: props.height })
const isMinimized = ref(false)

// 拖拽状态
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })

// 窗口样式
const windowStyle = computed(() => ({
  left: position.value.x + 'px',
  top: position.value.y + 'px',
  width: size.value.width + 'px',
  height: isMinimized.value ? '48px' : size.value.height + 'px',
  zIndex: props.zIndex
}))

// 开始拖拽
function startDrag(event) {
  isDragging.value = true
  dragOffset.value = {
    x: event.clientX - position.value.x,
    y: event.clientY - position.value.y
  }

  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  event.preventDefault()
}

// 拖拽中
function onDrag(event) {
  if (!isDragging.value) return

  const newX = event.clientX - dragOffset.value.x
  const newY = event.clientY - dragOffset.value.y

  // 限制在视窗内
  const maxX = window.innerWidth - size.value.width
  const maxY = window.innerHeight - size.value.height

  position.value = {
    x: Math.max(0, Math.min(newX, maxX)),
    y: Math.max(0, Math.min(newY, maxY))
  }

  emit('move', { id: props.id, x: position.value.x, y: position.value.y })
}

// 停止拖拽
function stopDrag() {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 切换最小化
function toggleMinimize() {
  isMinimized.value = !isMinimized.value
}

// 组件卸载时清理
onUnmounted(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
})

// 暴露方法
defineExpose({
  toggleMinimize,
  position,
  size
})
</script>

<style scoped>
.floating-window {
  position: absolute;
  background: rgba(255, 242, 250, 0.85);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 220, 235, 0.6);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.floating-window.active {
  box-shadow:
    0 12px 40px rgba(255, 158, 181, 0.15),
    0 4px 12px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  border-color: rgba(255, 180, 200, 0.7);
}

.floating-window.minimized {
  height: 48px !important;
}

/* 窗口头部 */
.window-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(255, 235, 245, 0.5);
  border-bottom: 1px solid rgba(255, 220, 235, 0.4);
  cursor: grab;
  user-select: none;
  flex-shrink: 0;
}

.window-header:active {
  cursor: grabbing;
}

.window-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.window-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.window-icon svg {
  width: 16px;
  height: 16px;
  color: #888;
}

.window-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.window-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.action-btn svg {
  width: 14px;
  height: 14px;
  color: #888;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.8);
}

.action-btn.close:hover {
  background: rgba(255, 107, 107, 0.2);
}

.action-btn.close:hover svg {
  color: #FF6B6B;
}

/* 窗口内容 */
.window-content {
  flex: 1;
  overflow: hidden;
  min-height: 0;
}
</style>
