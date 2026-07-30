<template>
  <!-- 带进入动画的列表容器 -->
  <TransitionGroup
    :name="animationName"
    :tag="tag"
    :class="containerClass"
    @before-enter="onBeforeEnter"
    @enter="onEnter"
    @leave="onLeave"
  >
    <slot></slot>
  </TransitionGroup>
</template>

<script setup>
/**
 * 带动画效果的列表组件
 * 支持列表项依次进入、离开动画
 */

const props = defineProps({
  tag: {
    type: String,
    default: 'div'
  },
  animation: {
    type: String,
    default: 'slide-up',
    validator: (val) => ['slide-up', 'slide-right', 'fade', 'scale'].includes(val)
  },
  stagger: {
    type: Number,
    default: 50 // 每项延迟（毫秒）
  },
  containerClass: {
    type: [String, Object, Array],
    default: ''
  }
})

const animationName = `list-${props.animation}`

// 进入前设置延迟
function onBeforeEnter(el) {
  el.style.opacity = '0'
  if (props.animation === 'slide-up') {
    el.style.transform = 'translateY(20px)'
  } else if (props.animation === 'slide-right') {
    el.style.transform = 'translateX(-20px)'
  } else if (props.animation === 'scale') {
    el.style.transform = 'scale(0.8)'
  }
}

// 进入动画
function onEnter(el, done) {
  const delay = el.dataset.index * props.stagger
  el.style.transition = `all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${delay}ms`

  requestAnimationFrame(() => {
    el.style.opacity = '1'
    el.style.transform = 'translateY(0) translateX(0) scale(1)'
  })

  setTimeout(done, delay + 300)
}

// 离开动画
function onLeave(el, done) {
  el.style.transition = 'all 0.2s ease-in'
  el.style.opacity = '0'

  if (props.animation === 'slide-up') {
    el.style.transform = 'translateY(-10px)'
  } else if (props.animation === 'slide-right') {
    el.style.transform = 'translateX(10px)'
  } else if (props.animation === 'scale') {
    el.style.transform = 'scale(0.8)'
  }

  setTimeout(done, 200)
}
</script>

<style>
/* 列表动画 */
.list-slide-up-enter-active,
.list-slide-right-enter-active,
.list-fade-enter-active,
.list-scale-enter-active {
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.list-slide-up-leave-active,
.list-slide-right-leave-active,
.list-fade-leave-active,
.list-scale-leave-active {
  transition: all 0.2s ease-in;
}

.list-slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.list-slide-up-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.list-slide-right-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.list-slide-right-leave-to {
  opacity: 0;
  transform: translateX(10px);
}

.list-fade-enter-from,
.list-fade-leave-to {
  opacity: 0;
}

.list-scale-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.list-scale-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

/* 移动动画 */
.list-slide-up-move,
.list-slide-right-move,
.list-fade-move,
.list-scale-move {
  transition: transform 0.3s ease;
}
</style>
