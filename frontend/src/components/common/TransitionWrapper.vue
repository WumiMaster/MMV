<template>
  <!-- 通用过渡动画包装器 -->
  <Transition
    :name="transitionName"
    :mode="mode"
    :duration="duration"
    @before-enter="$emit('before-enter', $event)"
    @enter="$emit('enter', $event)"
    @after-enter="$emit('after-enter', $event)"
    @before-leave="$emit('before-leave', $event)"
    @leave="$emit('leave', $event)"
    @after-leave="$emit('after-leave', $event)"
  >
    <slot></slot>
  </Transition>
</template>

<script setup>
/**
 * 通用过渡动画包装器
 * 封装常用的Vue Transition动画效果
 */

import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    default: 'fade',
    validator: (val) => [
      'fade', 'slide-up', 'slide-down', 'slide-left', 'slide-right',
      'scale', 'bounce', 'flip', 'zoom'
    ].includes(val)
  },
  mode: {
    type: String,
    default: 'out-in',
    validator: (val) => ['out-in', 'in-out', 'default'].includes(val)
  },
  duration: {
    type: [Number, Object],
    default: 300
  }
})

defineEmits([
  'before-enter', 'enter', 'after-enter',
  'before-leave', 'leave', 'after-leave'
])

const transitionName = computed(() => `transition-${props.name}`)
</script>

<style>
/* 淡入淡出 */
.transition-fade-enter-active,
.transition-fade-leave-active {
  transition: opacity 0.3s ease;
}

.transition-fade-enter-from,
.transition-fade-leave-to {
  opacity: 0;
}

/* 向上滑入 */
.transition-slide-up-enter-active {
  animation: slideUpIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.transition-slide-up-leave-active {
  animation: slideUpOut 0.2s ease-in forwards;
}

@keyframes slideUpIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUpOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-10px);
  }
}

/* 向下滑入 */
.transition-slide-down-enter-active {
  animation: slideDownIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.transition-slide-down-leave-active {
  animation: slideDownOut 0.2s ease-in forwards;
}

@keyframes slideDownIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDownOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(10px);
  }
}

/* 向左滑入 */
.transition-slide-left-enter-active {
  animation: slideLeftIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.transition-slide-left-leave-active {
  animation: slideLeftOut 0.2s ease-in forwards;
}

@keyframes slideLeftIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideLeftOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(-10px);
  }
}

/* 向右滑入 */
.transition-slide-right-enter-active {
  animation: slideRightIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.transition-slide-right-leave-active {
  animation: slideRightOut 0.2s ease-in forwards;
}

@keyframes slideRightIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideRightOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(10px);
  }
}

/* 缩放 */
.transition-scale-enter-active {
  animation: scaleIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.transition-scale-leave-active {
  animation: scaleOut 0.2s ease-in forwards;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes scaleOut {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.9);
  }
}

/* 弹性缩放 */
.transition-bounce-enter-active {
  animation: bounceIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.transition-bounce-leave-active {
  animation: bounceOut 0.3s ease-in forwards;
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes bounceOut {
  0% {
    transform: scale(1);
  }
  25% {
    transform: scale(0.95);
  }
  100% {
    opacity: 0;
    transform: scale(0.3);
  }
}

/* 翻转 */
.transition-flip-enter-active {
  animation: flipIn 0.4s ease-out;
}

.transition-flip-leave-active {
  animation: flipOut 0.3s ease-in forwards;
}

@keyframes flipIn {
  from {
    opacity: 0;
    transform: perspective(400px) rotateY(90deg);
  }
  to {
    opacity: 1;
    transform: perspective(400px) rotateY(0);
  }
}

@keyframes flipOut {
  from {
    opacity: 1;
    transform: perspective(400px) rotateY(0);
  }
  to {
    opacity: 0;
    transform: perspective(400px) rotateY(90deg);
  }
}

/* 缩放弹出 */
.transition-zoom-enter-active {
  animation: zoomIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.transition-zoom-leave-active {
  animation: zoomOut 0.2s ease-in forwards;
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes zoomOut {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.5);
  }
}
</style>
