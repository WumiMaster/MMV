<template>
  <!-- 频道列表侧边栏 -->
  <div class="channel-list">
    <div class="channel-list-header">
      <h3>我的频道</h3>
      <button class="icon-btn small" @click="$emit('join-channel')" title="加入频道">
        +
      </button>
    </div>

    <div class="channel-items">
      <div v-if="channels.length === 0" class="empty-tip">
        还没有加入任何频道
      </div>

      <div
        v-for="channel in channels"
        :key="channel.id"
        class="channel-item"
        :class="{ active: currentChannel?.id === channel.id }"
        @click="$emit('select-channel', channel)"
      >
        <div class="channel-icon">
          {{ channel.name.charAt(0) }}
        </div>
        <div class="channel-info">
          <div class="channel-name">{{ channel.name }}</div>
          <div class="channel-meta">{{ channel.member_count }} 成员</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 频道列表组件
 * 显示用户已加入的频道，支持选择和加入新频道
 */

defineProps({
  channels: {
    type: Array,
    default: () => []
  },
  currentChannel: {
    type: Object,
    default: null
  }
})

defineEmits(['select-channel', 'join-channel'])
</script>

<style scoped>
.channel-list {
  width: 240px;
  background: rgba(255, 255, 255, 0.3);
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.channel-list-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.4);
}

.channel-list-header h3 {
  font-size: 15px;
  font-weight: 600;
}

.icon-btn.small {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: rgba(126, 215, 167, 0.3);
  color: #2b8a3e;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  transition: all 0.15s;
}

.icon-btn.small:hover {
  background: rgba(126, 215, 167, 0.5);
  transform: scale(1.1);
}

.channel-items {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.empty-tip {
  padding: 20px;
  text-align: center;
  color: #999;
  font-size: 14px;
}

.channel-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.15s;
  margin-bottom: 4px;
}

.channel-item:hover {
  background: rgba(255, 255, 255, 0.4);
}

.channel-item.active {
  background: rgba(255, 158, 181, 0.2);
}

.channel-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
}

.channel-info {
  flex: 1;
  min-width: 0;
}

.channel-name {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.channel-meta {
  font-size: 12px;
  color: #999;
}
</style>
