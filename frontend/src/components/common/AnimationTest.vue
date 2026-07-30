<template>
  <!-- 动画测试组件 -->
  <div class="animation-test">
    <h2>动画系统测试</h2>

    <!-- 测试区域 -->
    <div class="test-section">
      <h3>1. 按钮动画测试</h3>
      <div class="test-group">
        <AnimatedButton variant="primary" @click="testClick('primary')">
          主要按钮
        </AnimatedButton>
        <AnimatedButton variant="secondary" @click="testClick('secondary')">
          次要按钮
        </AnimatedButton>
        <AnimatedButton variant="ghost" @click="testClick('ghost')">
          幽灵按钮
        </AnimatedButton>
        <AnimatedButton variant="danger" @click="testClick('danger')">
          危险按钮
        </AnimatedButton>
      </div>
      <div class="test-group">
        <AnimatedButton variant="primary" size="small">
          小按钮
        </AnimatedButton>
        <AnimatedButton variant="primary" size="medium">
          中按钮
        </AnimatedButton>
        <AnimatedButton variant="primary" size="large">
          大按钮
        </AnimatedButton>
      </div>
      <div class="test-group">
        <AnimatedButton variant="primary" :loading="isLoading" @click="testLoading">
          加载测试
        </AnimatedButton>
      </div>
    </div>

    <!-- 列表动画测试 -->
    <div class="test-section">
      <h3>2. 列表动画测试</h3>
      <div class="test-controls">
        <button @click="addListItem">添加项目</button>
        <button @click="removeListItem">移除项目</button>
        <button @click="shuffleList">随机排序</button>
      </div>
      <AnimatedList animation="slide-up" :stagger="50">
        <div v-for="item in listItems" :key="item.id" class="list-item">
          {{ item.text }}
        </div>
      </AnimatedList>
    </div>

    <!-- 过渡动画测试 -->
    <div class="test-section">
      <h3>3. 过渡动画测试</h3>
      <div class="test-controls">
        <select v-model="selectedTransition">
          <option value="fade">淡入淡出</option>
          <option value="slide-up">向上滑入</option>
          <option value="slide-down">向下滑入</option>
          <option value="scale">缩放</option>
          <option value="bounce">弹性</option>
          <option value="flip">翻转</option>
          <option value="zoom">变焦</option>
        </select>
        <button @click="toggleTransition">切换显示</button>
      </div>
      <TransitionWrapper :name="selectedTransition" mode="out-in">
        <div v-if="showTransition" key="content" class="transition-content">
          过渡动画内容
        </div>
        <div v-else key="placeholder" class="transition-placeholder">
          点击切换显示
        </div>
      </TransitionWrapper>
    </div>

    <!-- 通知测试 -->
    <div class="test-section">
      <h3>4. 通知动画测试</h3>
      <div class="test-controls">
        <button @click="testToast('success')">成功通知</button>
        <button @click="testToast('error')">错误通知</button>
        <button @click="testToast('warning')">警告通知</button>
        <button @click="testToast('info')">信息通知</button>
      </div>
    </div>

    <!-- 加载动画测试 -->
    <div class="test-section">
      <h3>5. 加载动画测试</h3>
      <div class="loading-grid">
        <div class="loading-item">
          <LoadingAnimation type="spinner" size="small" />
          <span>旋转加载</span>
        </div>
        <div class="loading-item">
          <LoadingAnimation type="pulse" size="small" />
          <span>脉冲加载</span>
        </div>
        <div class="loading-item">
          <LoadingAnimation type="wave" size="small" />
          <span>波浪加载</span>
        </div>
        <div class="loading-item">
          <LoadingAnimation type="bounce" size="small" />
          <span>弹跳加载</span>
        </div>
        <div class="loading-item">
          <LoadingAnimation type="meow" size="small" />
          <span>喵喵加载</span>
        </div>
      </div>
    </div>

    <!-- CSS 动画测试 -->
    <div class="test-section">
      <h3>6. CSS 动画测试</h3>
      <div class="css-animation-grid">
        <div class="css-anim-item pulse">脉冲</div>
        <div class="css-anim-item flash">闪烁</div>
        <div class="css-anim-item bounce">弹跳</div>
        <div class="css-anim-item shake">摇晃</div>
        <div class="css-anim-item wobble">抖动</div>
        <div class="css-anim-item swing">摆动</div>
        <div class="css-anim-item spin">旋转</div>
        <div class="css-anim-item float">悬浮</div>
        <div class="css-anim-item glow">发光</div>
      </div>
    </div>

    <!-- 交互动画测试 -->
    <div class="test-section">
      <h3>7. 交互动画测试</h3>
      <div class="interaction-grid">
        <div class="interaction-item tap-effect">
          点击效果
        </div>
        <div class="interaction-item hover-effect">
          悬浮效果
        </div>
        <div class="interaction-item focus-effect" tabindex="0">
          聚焦效果
        </div>
      </div>
    </div>

    <!-- 测试结果 -->
    <div class="test-section">
      <h3>测试结果</h3>
      <div class="test-results">
        <div v-for="result in testResults" :key="result.id" class="result-item">
          <span class="result-icon">{{ result.success ? '✅' : '❌' }}</span>
          <span class="result-text">{{ result.message }}</span>
        </div>
      </div>
    </div>

    <!-- 通知组件 -->
    <AnimatedToast ref="toastRef" />
  </div>
</template>

<script setup>
/**
 * 动画测试组件
 * 测试所有动画功能
 */

import { ref, nextTick } from 'vue'
import AnimatedButton from './AnimatedButton.vue'
import AnimatedList from './AnimatedList.vue'
import TransitionWrapper from './TransitionWrapper.vue'
import AnimatedToast from './AnimatedToast.vue'
import LoadingAnimation from './LoadingAnimation.vue'

// 通知引用
const toastRef = ref(null)

// 按钮测试
const isLoading = ref(false)

function testClick(type) {
  addTestResult(true, `${type} 按钮点击成功`)
}

function testLoading() {
  isLoading.value = true
  addTestResult(true, '加载状态触发')

  setTimeout(() => {
    isLoading.value = false
    addTestResult(true, '加载状态结束')
  }, 2000)
}

// 列表测试
const listItems = ref([
  { id: 1, text: '项目 1' },
  { id: 2, text: '项目 2' },
  { id: 3, text: '项目 3' }
])

let listId = 4

function addListItem() {
  listItems.value.push({
    id: listId++,
    text: `项目 ${listId - 1}`
  })
  addTestResult(true, '列表项目添加成功')
}

function removeListItem() {
  if (listItems.value.length > 0) {
    listItems.value.pop()
    addTestResult(true, '列表项目移除成功')
  }
}

function shuffleList() {
  listItems.value = [...listItems.value].sort(() => Math.random() - 0.5)
  addTestResult(true, '列表随机排序成功')
}

// 过渡测试
const selectedTransition = ref('fade')
const showTransition = ref(true)

function toggleTransition() {
  showTransition.value = !showTransition.value
  addTestResult(true, `过渡动画切换: ${selectedTransition.value}`)
}

// 通知测试
function testToast(type) {
  const messages = {
    success: '操作成功！',
    error: '操作失败，请重试',
    warning: '请注意检查',
    info: '这是一条信息'
  }

  toastRef.value[type](messages[type])
  addTestResult(true, `${type} 通知显示成功`)
}

// 测试结果
const testResults = ref([])
let resultId = 0

function addTestResult(success, message) {
  testResults.value.unshift({
    id: resultId++,
    success,
    message,
    time: new Date().toLocaleTimeString()
  })

  // 最多保留 10 条
  if (testResults.value.length > 10) {
    testResults.value.pop()
  }
}
</script>

<style scoped>
.animation-test {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

h3 {
  margin-bottom: 15px;
  color: #666;
  font-size: 16px;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.test-group {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.test-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.test-controls button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.test-controls button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 158, 181, 0.3);
}

.test-controls select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}

.list-item {
  padding: 10px 15px;
  margin-bottom: 8px;
  background: rgba(255, 240, 245, 0.6);
  border-radius: 10px;
  border: 1px solid rgba(200, 190, 198, 0.3);
}

.transition-content {
  padding: 20px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  border-radius: 12px;
  color: white;
  text-align: center;
  font-weight: 600;
}

.transition-placeholder {
  padding: 20px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  text-align: center;
  color: #666;
}

.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 15px;
}

.loading-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
}

.loading-item span {
  font-size: 12px;
  color: #666;
}

.css-animation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
}

.css-anim-item {
  padding: 15px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  border-radius: 12px;
  color: white;
  text-align: center;
  font-size: 12px;
  font-weight: 500;
}

.interaction-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
}

.interaction-item {
  padding: 20px;
  background: rgba(255, 240, 245, 0.6);
  border-radius: 12px;
  text-align: center;
  font-size: 14px;
  color: #333;
  cursor: pointer;
}

.test-results {
  max-height: 200px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  margin-bottom: 5px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  font-size: 13px;
}

.result-icon {
  font-size: 14px;
}

.result-text {
  flex: 1;
  color: #333;
}

/* CSS 动画类 */
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

/* 交互动画 */
.tap-effect {
  transition: transform 0.1s ease;
}

.tap-effect:active {
  transform: scale(0.95);
}

.hover-effect {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-effect:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.focus-effect {
  transition: box-shadow 0.2s ease;
  outline: none;
}

.focus-effect:focus {
  box-shadow: 0 0 0 3px rgba(255, 158, 181, 0.3);
}

/* 关键帧 */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes flash {
  0%, 50%, 100% { opacity: 1; }
  25%, 75% { opacity: 0; }
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% { animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1); transform: translate3d(0, 0, 0); }
  40%, 43% { animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06); transform: translate3d(0, -30px, 0); }
  70% { animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06); transform: translate3d(0, -15px, 0); }
  90% { transform: translate3d(0, -4px, 0); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
  20%, 40%, 60%, 80% { transform: translateX(10px); }
}

@keyframes wobble {
  0% { transform: none; }
  15% { transform: translate3d(-25%, 0, 0) rotate3d(0, 0, 1, -5deg); }
  30% { transform: translate3d(20%, 0, 0) rotate3d(0, 0, 1, 3deg); }
  45% { transform: translate3d(-15%, 0, 0) rotate3d(0, 0, 1, -3deg); }
  60% { transform: translate3d(10%, 0, 0) rotate3d(0, 0, 1, 2deg); }
  75% { transform: translate3d(-5%, 0, 0) rotate3d(0, 0, 1, -1deg); }
  100% { transform: none; }
}

@keyframes swing {
  20% { transform: rotate3d(0, 0, 1, 15deg); }
  40% { transform: rotate3d(0, 0, 1, -10deg); }
  60% { transform: rotate3d(0, 0, 1, 5deg); }
  80% { transform: rotate3d(0, 0, 1, -5deg); }
  100% { transform: rotate3d(0, 0, 1, 0deg); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px rgba(255, 158, 181, 0.5); }
  50% { box-shadow: 0 0 20px rgba(255, 158, 181, 0.8); }
}

/* 响应式 */
@media (max-width: 768px) {
  .animation-test {
    padding: 10px;
  }

  .test-group,
  .test-controls {
    flex-direction: column;
  }

  .loading-grid,
  .css-animation-grid,
  .interaction-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
