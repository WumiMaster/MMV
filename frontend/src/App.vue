<template>
  <div class="app-container">
    <!-- 路由视图 -->
    <router-view />
  </div>
</template>

<script setup>
// 根组件
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #FFF5F8 0%, #ffe8f0 50%, #e8f9ef 100%);
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.app-container::before,
.app-container::after {
  content: '';
  position: fixed;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.5;
  pointer-events: none;
  z-index: 0;
}

.app-container::before {
  width: 400px;
  height: 400px;
  background: #FF9EB5;
  top: -100px;
  right: -100px;
}

.app-container::after {
  width: 300px;
  height: 300px;
  background: #7ED7A7;
  bottom: -80px;
  left: -80px;
}
</style>
