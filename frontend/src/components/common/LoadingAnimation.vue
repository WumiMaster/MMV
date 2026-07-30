<template>
  <!-- 加载动画组件 -->
  <div class="loading-container" :class="[size, { overlay: overlay }]">
    <!-- 骨架屏加载 -->
    <div v-if="type === 'skeleton'" class="skeleton-wrapper">
      <div class="skeleton-avatar"></div>
      <div class="skeleton-content">
        <div class="skeleton-line" style="width: 80%"></div>
        <div class="skeleton-line" style="width: 60%"></div>
      </div>
    </div>

    <!-- 脉冲加载 -->
    <div v-else-if="type === 'pulse'" class="pulse-wrapper">
      <div class="pulse-dot" v-for="i in 3" :key="i" :style="{ animationDelay: i * 0.15 + 's' }"></div>
    </div>

    <!-- 旋转加载 -->
    <div v-else-if="type === 'spinner'" class="spinner-wrapper">
      <div class="spinner"></div>
    </div>

    <!-- 波浪加载 -->
    <div v-else-if="type === 'wave'" class="wave-wrapper">
      <div class="wave-bar" v-for="i in 5" :key="i" :style="{ animationDelay: i * 0.1 + 's' }"></div>
    </div>

    <!-- 弹跳加载 -->
    <div v-else-if="type === 'bounce'" class="bounce-wrapper">
      <div class="bounce-ball" v-for="i in 3" :key="i" :style="{ animationDelay: i * 0.16 + 's' }"></div>
    </div>

    <!-- 喵喵加载（品牌特色） -->
    <div v-else-if="type === 'meow'" class="meow-wrapper">
      <div class="meow-paw" v-for="i in 4" :key="i" :style="{ animationDelay: i * 0.2 + 's' }">🐾</div>
    </div>

    <!-- 默认加载 -->
    <div v-else class="default-wrapper">
      <div class="default-spinner"></div>
    </div>

    <!-- 加载文字 -->
    <p v-if="text" class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup>
/**
 * 加载动画组件
 * 支持多种动画类型和尺寸
 */

defineProps({
  type: {
    type: String,
    default: 'spinner',
    validator: (val) => ['skeleton', 'pulse', 'spinner', 'wave', 'bounce', 'meow', 'default'].includes(val)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (val) => ['small', 'medium', 'large'].includes(val)
  },
  text: {
    type: String,
    default: ''
  },
  overlay: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.loading-container.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  z-index: 9999;
}

/* 尺寸 */
.loading-container.small {
  padding: 8px;
}

.loading-container.medium {
  padding: 16px;
}

.loading-container.large {
  padding: 32px;
}

/* 骨架屏 */
.skeleton-wrapper {
  display: flex;
  gap: 12px;
  width: 100%;
  max-width: 300px;
}

.skeleton-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(
    90deg,
    rgba(255, 240, 245, 0.6) 0%,
    rgba(255, 220, 235, 0.8) 50%,
    rgba(255, 240, 245, 0.6) 100%
  );
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.skeleton-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-line {
  height: 14px;
  border-radius: 7px;
  background: linear-gradient(
    90deg,
    rgba(255, 240, 245, 0.6) 0%,
    rgba(255, 220, 235, 0.8) 50%,
    rgba(255, 240, 245, 0.6) 100%
  );
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

@keyframes skeleton-loading {
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: calc(200px + 100%) 0;
  }
}

/* 脉冲 */
.pulse-wrapper {
  display: flex;
  gap: 8px;
}

.pulse-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  animation: pulse 1.4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 旋转 */
.spinner-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 158, 181, 0.2);
  border-top-color: #FF9EB5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 波浪 */
.wave-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 32px;
}

.wave-bar {
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #FF9EB5, #7ED7A7);
  border-radius: 2px;
  animation: wave 1.2s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% {
    transform: scaleY(0.4);
  }
  50% {
    transform: scaleY(1);
  }
}

/* 弹跳 */
.bounce-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bounce-ball {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9EB5, #FFB8CC);
  animation: bounce 1.4s ease-in-out infinite;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-15px);
  }
}

/* 喵喵 */
.meow-wrapper {
  display: flex;
  gap: 8px;
}

.meow-paw {
  font-size: 24px;
  animation: meow 1.6s ease-in-out infinite;
}

@keyframes meow {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
    opacity: 0.5;
  }
  50% {
    transform: translateY(-10px) rotate(10deg);
    opacity: 1;
  }
}

/* 默认 */
.default-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.default-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 158, 181, 0.2);
  border-top-color: #FF9EB5;
  border-right-color: #7ED7A7;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 加载文字 */
.loading-text {
  font-size: 14px;
  color: #888;
  text-align: center;
  margin: 0;
}

/* 尺寸调整 */
.loading-container.small .spinner,
.loading-container.small .default-spinner {
  width: 20px;
  height: 20px;
  border-width: 2px;
}

.loading-container.large .spinner,
.loading-container.large .default-spinner {
  width: 48px;
  height: 48px;
  border-width: 4px;
}

.loading-container.small .pulse-dot,
.loading-container.small .bounce-ball {
  width: 8px;
  height: 8px;
}

.loading-container.large .pulse-dot,
.loading-container.large .bounce-ball {
  width: 16px;
  height: 16px;
}

.loading-container.small .meow-paw {
  font-size: 16px;
}

.loading-container.large .meow-paw {
  font-size: 32px;
}

.loading-container.small .loading-text {
  font-size: 12px;
}

.loading-container.large .loading-text {
  font-size: 16px;
}
</style>
