<template>
  <!-- 带动画的弹窗容器 -->
  <Teleport to="body">
    <Transition name="modal" @after-leave="$emit('closed')">
      <div
        v-if="visible"
        class="modal-overlay"
        @click.self="$emit('close')"
      >
        <div class="modal-content" :class="modalClass">
          <slot></slot>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
/**
 * 带开关动画的弹窗容器
 * 使用 Vue Transition 组件实现平滑的开关动画
 */

defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  modalClass: {
    type: String,
    default: ''
  }
})

defineEmits(['close', 'closed'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  max-width: 90%;
  max-height: 90vh;
}
</style>
