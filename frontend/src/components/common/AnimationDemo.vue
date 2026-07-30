<template>
  <!-- 动画演示组件 -->
  <div class="animation-demo">
    <h3>动画效果演示</h3>

    <!-- 进入动画 -->
    <div class="demo-section">
      <h4>进入动画</h4>
      <div class="demo-grid">
        <button
          v-for="anim in enterAnimations"
          :key="anim.name"
          class="demo-btn"
          @click="playAnimation(anim.name)"
        >
          {{ anim.label }}
        </button>
      </div>
    </div>

    <!-- 退出动画 -->
    <div class="demo-section">
      <h4>退出动画</h4>
      <div class="demo-grid">
        <button
          v-for="anim in exitAnimations"
          :key="anim.name"
          class="demo-btn"
          @click="playAnimation(anim.name)"
        >
          {{ anim.label }}
        </button>
      </div>
    </div>

    <!-- 强调动画 -->
    <div class="demo-section">
      <h4>强调动画</h4>
      <div class="demo-grid">
        <button
          v-for="anim in emphasisAnimations"
          :key="anim.name"
          class="demo-btn"
          @click="playAnimation(anim.name)"
        >
          {{ anim.label }}
        </button>
      </div>
    </div>

    <!-- 特效动画 -->
    <div class="demo-section">
      <h4>特效动画</h4>
      <div class="demo-grid">
        <button
          v-for="anim in effectAnimations"
          :key="anim.name"
          class="demo-btn"
          @click="playAnimation(anim.name)"
        >
          {{ anim.label }}
        </button>
      </div>
    </div>

    <!-- 动画预览区域 -->
    <div class="preview-area">
      <div
        ref="previewElement"
        class="preview-box"
        :class="currentAnimation"
        @animationend="onAnimationEnd"
      >
        <span class="preview-icon">🐱</span>
        <span class="preview-text">喵喵</span>
      </div>
    </div>

    <!-- 动画控制 -->
    <div class="controls">
      <button class="control-btn" @click="resetAnimation">
        重置
      </button>
      <button class="control-btn" @click="playCurrentAnimation">
        播放
      </button>
    </div>
  </div>
</template>

<script setup>
/**
 * 动画演示组件
 * 展示各种动画效果
 */

import { ref, nextTick } from 'vue'

const previewElement = ref(null)
const currentAnimation = ref('')
const isAnimating = ref(false)

// 进入动画列表
const enterAnimations = [
  { name: 'fade-in', label: '淡入' },
  { name: 'fade-in-up', label: '上淡入' },
  { name: 'fade-in-down', label: '下淡入' },
  { name: 'fade-in-left', label: '左淡入' },
  { name: 'fade-in-right', label: '右淡入' },
  { name: 'slide-in-up', label: '上滑入' },
  { name: 'slide-in-down', label: '下滑入' },
  { name: 'slide-in-left', label: '左滑入' },
  { name: 'slide-in-right', label: '右滑入' },
  { name: 'scale-in', label: '缩放进入' },
  { name: 'bounce-in', label: '弹入' },
  { name: 'bounce-in-up', label: '上弹入' },
  { name: 'bounce-in-down', label: '下弹入' },
  { name: 'flip-in', label: '翻转进入' },
  { name: 'rotate-in', label: '旋转进入' }
]

// 退出动画列表
const exitAnimations = [
  { name: 'fade-out', label: '淡出' },
  { name: 'fade-out-up', label: '上淡出' },
  { name: 'fade-out-down', label: '下淡出' },
  { name: 'fade-out-left', label: '左淡出' },
  { name: 'fade-out-right', label: '右淡出' },
  { name: 'slide-out-up', label: '上滑出' },
  { name: 'slide-out-down', label: '下滑出' },
  { name: 'slide-out-left', label: '左滑出' },
  { name: 'slide-out-right', label: '右滑出' },
  { name: 'scale-out', label: '缩放退出' },
  { name: 'bounce-out', label: '弹出' },
  { name: 'bounce-out-up', label: '上弹出' },
  { name: 'bounce-out-down', label: '下弹出' }
]

// 强调动画列表
const emphasisAnimations = [
  { name: 'pulse', label: '脉冲' },
  { name: 'flash', label: '闪烁' },
  { name: 'bounce', label: '弹跳' },
  { name: 'shake', label: '摇晃' },
  { name: 'wobble', label: '抖动' },
  { name: 'swing', label: '摆动' },
  { name: 'spin', label: '旋转' }
]

// 特效动画列表
const effectAnimations = [
  { name: 'float', label: '悬浮' },
  { name: 'glow', label: '发光' },
  { name: 'jelly', label: '果冻' },
  { name: 'wobble-soft', label: '轻晃' },
  { name: 'bounce-cute', label: '可爱弹跳' },
  { name: 'jump-happy', label: '开心跳动' },
  { name: 'land-soft', label: '软着陆' },
  { name: 'elastic-in', label: '弹性进入' },
  { name: 'elastic-out', label: '弹性退出' }
]

// 播放动画
function playAnimation(animationName) {
  if (isAnimating.value) return

  isAnimating.value = true
  currentAnimation.value = ''

  nextTick(() => {
    currentAnimation.value = animationName
  })
}

// 播放当前动画
function playCurrentAnimation() {
  if (currentAnimation.value) {
    playAnimation(currentAnimation.value)
  }
}

// 重置动画
function resetAnimation() {
  isAnimating.value = false
  currentAnimation.value = ''
}

// 动画结束
function onAnimationEnd() {
  isAnimating.value = false
}
</script>

<style scoped>
.animation-demo {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto;
}

h3 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

h4 {
  margin-bottom: 10px;
  color: #666;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.demo-section {
  margin-bottom: 20px;
}

.demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 8px;
}

.demo-btn {
  padding: 8px 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  color: white;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.demo-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 158, 181, 0.3);
}

.demo-btn:active {
  transform: translateY(0);
}

.preview-area {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 150px;
  margin: 20px 0;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 12px;
}

.preview-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  border-radius: 20px;
  box-shadow: 0 4px 16px rgba(255, 158, 181, 0.4);
}

.preview-icon {
  font-size: 32px;
  margin-bottom: 4px;
}

.preview-text {
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.control-btn {
  padding: 10px 24px;
  border: none;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.05);
  color: #666;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

/* 动画类 */
.fade-in {
  animation: fadeIn 0.3s ease forwards;
}

.fade-in-up {
  animation: fadeInUp 0.3s ease forwards;
}

.fade-in-down {
  animation: fadeInDown 0.3s ease forwards;
}

.fade-in-left {
  animation: fadeInLeft 0.3s ease forwards;
}

.fade-in-right {
  animation: fadeInRight 0.3s ease forwards;
}

.slide-in-up {
  animation: slideInUp 0.3s ease forwards;
}

.slide-in-down {
  animation: slideInDown 0.3s ease forwards;
}

.slide-in-left {
  animation: slideInLeft 0.3s ease forwards;
}

.slide-in-right {
  animation: slideInRight 0.3s ease forwards;
}

.scale-in {
  animation: scaleIn 0.3s ease forwards;
}

.bounce-in {
  animation: bounceIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}

.bounce-in-up {
  animation: bounceInUp 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}

.bounce-in-down {
  animation: bounceInDown 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}

.flip-in {
  animation: flipIn 0.4s ease forwards;
}

.rotate-in {
  animation: rotateIn 0.3s ease forwards;
}

.fade-out {
  animation: fadeOut 0.2s ease forwards;
}

.fade-out-up {
  animation: fadeOutUp 0.2s ease forwards;
}

.fade-out-down {
  animation: fadeOutDown 0.2s ease forwards;
}

.fade-out-left {
  animation: fadeOutLeft 0.2s ease forwards;
}

.fade-out-right {
  animation: fadeOutRight 0.2s ease forwards;
}

.slide-out-up {
  animation: slideOutUp 0.2s ease forwards;
}

.slide-out-down {
  animation: slideOutDown 0.2s ease forwards;
}

.slide-out-left {
  animation: slideOutLeft 0.2s ease forwards;
}

.slide-out-right {
  animation: slideOutRight 0.2s ease forwards;
}

.scale-out {
  animation: scaleOut 0.2s ease forwards;
}

.bounce-out {
  animation: bounceOut 0.3s ease forwards;
}

.bounce-out-up {
  animation: bounceOutUp 0.3s ease forwards;
}

.bounce-out-down {
  animation: bounceOutDown 0.3s ease forwards;
}

.pulse {
  animation: pulse 1s ease-in-out infinite;
}

.flash {
  animation: flash 1s linear infinite;
}

.bounce {
  animation: bounce 1s ease infinite;
}

.shake {
  animation: shake 0.5s ease;
}

.wobble {
  animation: wobble 0.5s ease;
}

.swing {
  animation: swing 0.5s ease;
}

.spin {
  animation: spin 1s linear infinite;
}

.float {
  animation: float 3s ease-in-out infinite;
}

.glow {
  animation: glow 2s ease-in-out infinite;
}

.jelly {
  animation: softSquish 0.5s ease;
}

.wobble-soft {
  animation: gentleWobble 0.5s ease;
}

.bounce-cute {
  animation: cuteBounce 0.6s ease;
}

.jump-happy {
  animation: happyJump 0.6s ease;
}

.land-soft {
  animation: softLand 0.5s ease;
}

.elastic-in {
  animation: elasticIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}

.elastic-out {
  animation: elasticOut 0.4s ease forwards;
}
</style>
