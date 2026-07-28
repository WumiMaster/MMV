<template>
  <!-- 频道管理组件 -->
  <div class="channel-manage">
    <div class="section-header">
      <div class="section-title">频道管理</div>
      <button class="btn-green" @click="showCreateChannelModal = true">
        + 创建频道
      </button>
    </div>

    <!-- 频道列表 -->
    <div class="channel-table-container">
      <table class="channel-table">
        <thead>
          <tr>
            <th>频道名称</th>
            <th>频道 ID</th>
            <th>成员数</th>
            <th>子频道数</th>
            <th>消息留存</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="channel in channels" :key="channel.id">
            <td>{{ channel.name }}</td>
            <td>
              <span class="channel-id-badge">{{ channel.channel_id }}</span>
            </td>
            <td>{{ channel.member_count }}</td>
            <td>{{ channel.sub_channel_count }}</td>
            <td>{{ channel.message_retention_days }} 天</td>
            <td>
              <div class="action-btns">
                <button class="btn-edit" @click="manageSubChannels(channel)">子频道</button>
                <button class="btn-edit" @click="editChannel(channel)">编辑</button>
                <button class="btn-delete" @click="confirmDeleteChannel(channel)">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <button :disabled="currentPage <= 1" @click="loadChannels(currentPage - 1)">上一页</button>
      <span>第 {{ currentPage }} / {{ totalChannelPages }} 页</span>
      <button :disabled="currentPage >= totalChannelPages" @click="loadChannels(currentPage + 1)">下一页</button>
    </div>

    <!-- 创建频道弹窗 -->
    <Teleport to="body">
      <div v-if="showCreateChannelModal" class="modal-overlay animate-overlay-in" @click.self="showCreateChannelModal = false">
        <div class="glass-card modal animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">创建频道</div>
            <button class="modal-close" @click="showCreateChannelModal = false">×</button>
          </div>

          <div class="form-group">
            <label class="form-label">频道名称 *</label>
            <input v-model="channelForm.name" type="text" class="glass-input" placeholder="请输入频道名称" />
          </div>

          <div class="form-group">
            <label class="form-label">频道 ID（留空自动生成）</label>
            <input v-model="channelForm.channel_id" type="text" class="glass-input" placeholder="自定义频道ID或留空" />
          </div>

          <div class="form-group">
            <label class="form-label">频道描述</label>
            <textarea v-model="channelForm.description" class="glass-input textarea" placeholder="频道描述（可选）"></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">消息留存天数</label>
            <input v-model.number="channelForm.message_retention_days" type="number" class="glass-input" min="1" max="365" />
          </div>

          <div class="modal-footer">
            <button class="btn-cancel" @click="showCreateChannelModal = false">取消</button>
            <button class="btn-primary" @click="handleCreateChannel" :disabled="!channelForm.name">确认创建</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 编辑频道弹窗 -->
    <Teleport to="body">
      <div v-if="showEditChannelModal" class="modal-overlay animate-overlay-in" @click.self="showEditChannelModal = false">
        <div class="glass-card modal animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">编辑频道</div>
            <button class="modal-close" @click="showEditChannelModal = false">×</button>
          </div>

          <div class="form-group">
            <label class="form-label">频道名称</label>
            <input v-model="editChannelForm.name" type="text" class="glass-input" />
          </div>

          <div class="form-group">
            <label class="form-label">频道描述</label>
            <textarea v-model="editChannelForm.description" class="glass-input textarea"></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">消息留存天数</label>
            <input v-model.number="editChannelForm.message_retention_days" type="number" class="glass-input" min="1" max="365" />
          </div>

          <div class="modal-footer">
            <button class="btn-cancel" @click="showEditChannelModal = false">取消</button>
            <button class="btn-primary" @click="handleUpdateChannel">保存修改</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 子频道管理弹窗 -->
    <Teleport to="body">
      <div v-if="showSubChannelModal" class="modal-overlay animate-overlay-in" @click.self="showSubChannelModal = false">
        <div class="glass-card modal large animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">子频道管理 - {{ currentManageChannel?.name }}</div>
            <button class="modal-close" @click="showSubChannelModal = false">×</button>
          </div>

          <div class="sub-channel-list">
            <div v-if="subChannels.length === 0" class="empty-tip">暂无子频道</div>

            <div v-for="sc in subChannels" :key="sc.id" class="sub-channel-item">
              <span v-if="sc.type === 'text'" class="sc-icon">#</span>
              <svg v-else class="sc-icon voice-icon-admin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" y1="19" x2="12" y2="23"></line>
                <line x1="8" y1="23" x2="16" y2="23"></line>
              </svg>
              <span class="sc-name">{{ sc.name }}</span>
              <span class="sc-type">{{ sc.type === 'text' ? '文字' : '语音' }}</span>
              <div class="sc-actions">
                <button class="btn-edit small" @click="editSubChannel(sc)">编辑</button>
                <button class="btn-delete small" @click="confirmDeleteSubChannel(sc)">删除</button>
              </div>
            </div>
          </div>

          <button class="btn-green full-width" @click="showCreateSubChannelModal = true">
            + 添加子频道
          </button>
        </div>
      </div>
    </Teleport>

    <!-- 创建子频道弹窗 -->
    <Teleport to="body">
      <div v-if="showCreateSubChannelModal" class="modal-overlay animate-overlay-in" @click.self="showCreateSubChannelModal = false">
        <div class="glass-card modal animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">添加子频道</div>
            <button class="modal-close" @click="showCreateSubChannelModal = false">×</button>
          </div>

          <div class="form-group">
            <label class="form-label">子频道名称 *</label>
            <input v-model="subChannelForm.name" type="text" class="glass-input" placeholder="请输入子频道名称" />
          </div>

          <div class="form-group">
            <label class="form-label">类型</label>
            <select v-model="subChannelForm.type" class="glass-input">
              <option value="text">文字频道</option>
              <option value="voice">语音频道</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">排序号（越小越靠前）</label>
            <input v-model.number="subChannelForm.sort_order" type="number" class="glass-input" min="0" />
          </div>

          <div class="modal-footer">
            <button class="btn-cancel" @click="showCreateSubChannelModal = false">取消</button>
            <button class="btn-primary" @click="handleCreateSubChannel" :disabled="!subChannelForm.name">确认添加</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 删除确认弹窗 -->
    <Teleport to="body">
      <div v-if="showDeleteModal" class="modal-overlay animate-overlay-in" @click.self="showDeleteModal = false">
        <div class="glass-card modal animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">确认删除</div>
            <button class="modal-close" @click="showDeleteModal = false">×</button>
          </div>

          <p class="modal-desc">
            确定要删除 <strong>{{ deleteTarget?.name }}</strong> 吗？<br />
            此操作不可撤销。
          </p>

          <div class="modal-footer">
            <button class="btn-cancel" @click="showDeleteModal = false">取消</button>
            <button class="btn-danger" @click="handleDelete">确认删除</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Toast 提示 -->
    <div v-if="toast.show" class="toast" :class="toast.type">
      {{ toast.message }}
    </div>
  </div>
</template>

<script setup>
/**
 * 频道管理组件
 * 管理员创建、编辑、删除频道和子频道
 */

import { ref, computed, onMounted } from 'vue'
import api from '../../api'

// 频道数据
const channels = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalChannels = ref(0)
const totalChannelPages = computed(() => Math.ceil(totalChannels.value / pageSize.value))

// 弹窗状态
const showCreateChannelModal = ref(false)
const showEditChannelModal = ref(false)
const showSubChannelModal = ref(false)
const showCreateSubChannelModal = ref(false)
const showDeleteModal = ref(false)

// 表单数据
const channelForm = ref({
  name: '',
  channel_id: '',
  description: '',
  message_retention_days: 30
})

const editChannelForm = ref({
  id: null,
  name: '',
  description: '',
  message_retention_days: 30
})

const subChannelForm = ref({
  name: '',
  type: 'text',
  sort_order: 0
})

// 当前管理的频道
const currentManageChannel = ref(null)
const subChannels = ref([])

// 删除目标
const deleteTarget = ref(null)
const deleteType = ref('channel') // 'channel' | 'sub_channel'

// Toast 提示
const toast = ref({ show: false, message: '', type: 'success' })

function showToast(message, type = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => {
    toast.value.show = false
  }, 2000)
}

// 加载频道列表
async function loadChannels(page = 1) {
  try {
    const response = await api.get('/api/admin/channels', {
      params: { page, page_size: pageSize.value }
    })
    channels.value = response.data.channels
    totalChannels.value = response.data.total
    currentPage.value = page
  } catch (error) {
    showToast('加载频道列表失败', 'error')
  }
}

// 创建频道
async function handleCreateChannel() {
  if (!channelForm.value.name) return

  try {
    await api.post('/api/admin/channels', channelForm.value)
    showToast('频道创建成功')
    showCreateChannelModal.value = false
    channelForm.value = { name: '', channel_id: '', description: '', message_retention_days: 30 }
    loadChannels(currentPage.value)
  } catch (error) {
    showToast(error.response?.data?.detail || '创建失败', 'error')
  }
}

// 编辑频道
function editChannel(channel) {
  editChannelForm.value = {
    id: channel.id,
    name: channel.name,
    description: channel.description || '',
    message_retention_days: channel.message_retention_days
  }
  showEditChannelModal.value = true
}

// 更新频道
async function handleUpdateChannel() {
  try {
    await api.put(`/api/admin/channels/${editChannelForm.value.id}`, {
      name: editChannelForm.value.name,
      description: editChannelForm.value.description,
      message_retention_days: editChannelForm.value.message_retention_days
    })
    showToast('频道信息已更新')
    showEditChannelModal.value = false
    loadChannels(currentPage.value)
  } catch (error) {
    showToast(error.response?.data?.detail || '更新失败', 'error')
  }
}

// 确认删除频道
function confirmDeleteChannel(channel) {
  deleteTarget.value = channel
  deleteType.value = 'channel'
  showDeleteModal.value = true
}

// 执行删除
async function handleDelete() {
  try {
    if (deleteType.value === 'channel') {
      await api.delete(`/api/admin/channels/${deleteTarget.value.id}`)
      showToast('频道已删除')
      loadChannels(currentPage.value)
    } else {
      await api.delete(`/api/admin/sub-channels/${deleteTarget.value.id}`)
      showToast('子频道已删除')
      loadSubChannels(currentManageChannel.value.id)
    }
    showDeleteModal.value = false
  } catch (error) {
    showToast(error.response?.data?.detail || '删除失败', 'error')
  }
}

// 管理子频道
async function manageSubChannels(channel) {
  currentManageChannel.value = channel
  await loadSubChannels(channel.id)
  showSubChannelModal.value = true
}

// 加载子频道列表
async function loadSubChannels(channelId) {
  try {
    const response = await api.get(`/api/channels/${channelId}`)
    subChannels.value = response.data.sub_channels
  } catch (error) {
    showToast('加载子频道失败', 'error')
  }
}

// 创建子频道
async function handleCreateSubChannel() {
  if (!subChannelForm.value.name || !currentManageChannel.value) return

  try {
    await api.post(`/api/admin/channels/${currentManageChannel.value.id}/sub-channels`, subChannelForm.value)
    showToast('子频道添加成功')
    showCreateSubChannelModal.value = false
    subChannelForm.value = { name: '', type: 'text', sort_order: 0 }
    loadSubChannels(currentManageChannel.value.id)
    loadChannels(currentPage.value)
  } catch (error) {
    showToast(error.response?.data?.detail || '添加失败', 'error')
  }
}

// 编辑子频道
function editSubChannel(sc) {
  // 简化处理：直接弹出编辑框
  const newName = prompt('请输入新的子频道名称', sc.name)
  if (newName && newName !== sc.name) {
    handleUpdateSubChannel(sc.id, newName)
  }
}

// 更新子频道
async function handleUpdateSubChannel(subChannelId, name) {
  try {
    await api.put(`/api/admin/sub-channels/${subChannelId}`, { name })
    showToast('子频道已更新')
    loadSubChannels(currentManageChannel.value.id)
  } catch (error) {
    showToast('更新失败', 'error')
  }
}

// 确认删除子频道
function confirmDeleteSubChannel(sc) {
  deleteTarget.value = sc
  deleteType.value = 'sub_channel'
  showDeleteModal.value = true
}

// 页面加载
onMounted(() => {
  loadChannels()
})
</script>

<style scoped>
.channel-manage {
  padding: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.btn-green {
  height: 42px;
  padding: 0 20px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #7ED7A7, #A0E8C0);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 15px rgba(126, 215, 167, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-green:hover {
  box-shadow: 0 6px 20px rgba(126, 215, 167, 0.45);
  background: linear-gradient(135deg, #90E0B5, #B0F0C8);
}

.btn-green.full-width {
  width: 100%;
  margin-top: 16px;
}

/* 表格 */
.channel-table-container {
  overflow-x: auto;
}

.channel-table {
  width: 100%;
  border-collapse: collapse;
}

.channel-table th,
.channel-table td {
  padding: 14px 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}

.channel-table th {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
}

.channel-table tr:hover td {
  background: rgba(255, 255, 255, 0.3);
}

.channel-id-badge {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(126, 215, 167, 0.2);
  border-radius: 8px;
  font-size: 13px;
  font-family: monospace;
  color: #2b8a3e;
}

.action-btns {
  display: flex;
  gap: 8px;
}

.btn-edit {
  padding: 6px 14px;
  border: 1px solid #7ED7A7;
  background: transparent;
  color: #7ED7A7;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s ease, color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-edit:hover {
  background: #7ED7A7;
  color: white;
}

.btn-edit.small {
  padding: 4px 10px;
  font-size: 12px;
}

.btn-delete {
  padding: 6px 14px;
  border: none;
  background: transparent;
  color: #FF6B6B;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-delete:hover {
  background: rgba(255, 107, 107, 0.1);
}

.btn-delete.small {
  padding: 4px 10px;
  font-size: 12px;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
  font-size: 14px;
  color: #666;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid rgba(200, 190, 198, 0.5);
  background: rgba(255, 245, 250, 0.6);
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination button:hover:not(:disabled) {
  background: rgba(255, 238, 245, 0.7);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 弹窗 */
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

.modal {
  width: 90%;
  max-width: 440px;
  padding: 28px;
}

.modal.large {
  max-width: 600px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 220, 230, 0.4);
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(255, 235, 240, 0.6);
  border-radius: 10px;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
  color: #666;
}

.modal-close:hover {
  background: rgba(255, 220, 230, 0.7);
}

.modal-desc {
  color: #666;
  line-height: 1.6;
  margin-bottom: 24px;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #444;
}

.textarea {
  min-height: 80px;
  padding: 12px;
  resize: vertical;
}

.modal-footer {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 220, 230, 0.4);
}

.modal-footer button {
  flex: 1;
  height: 44px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  border: none;
  background: linear-gradient(135deg, #FF9EB5, #FFB8CC);
  color: white;
  box-shadow: 0 3px 12px rgba(255, 158, 181, 0.35);
}

.btn-primary:hover:not(:disabled) {
  box-shadow: 0 5px 16px rgba(255, 158, 181, 0.45);
  background: linear-gradient(135deg, #FFB0C5, #FFC8D8);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  border: 1px solid rgba(200, 190, 198, 0.5);
  background: rgba(255, 245, 250, 0.6);
  color: #666;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.btn-cancel:hover {
  background: rgba(255, 238, 245, 0.7);
  border-color: rgba(200, 190, 198, 0.6);
}

.btn-danger {
  flex: 1;
  height: 44px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #FF6B6B, #ff8787);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 3px 12px rgba(255, 107, 107, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-danger:hover {
  box-shadow: 0 5px 16px rgba(255, 107, 107, 0.4);
  background: linear-gradient(135deg, #FF7B7B, #ff9797);
}

/* 子频道列表 */
.sub-channel-list {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.empty-tip {
  text-align: center;
  color: #999;
  padding: 24px;
  font-size: 14px;
  background: rgba(255, 245, 250, 0.3);
  border-radius: 10px;
}

.sub-channel-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 8px;
  background: rgba(255, 242, 248, 0.4);
  border: 1px solid rgba(220, 210, 218, 0.35);
  transition: background 0.2s ease;
}

.sub-channel-item:hover {
  background: rgba(255, 235, 242, 0.5);
}

.sc-icon {
  font-size: 18px;
  color: #888;
  font-weight: 600;
}

.voice-icon-admin {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #888;
}

.sc-name {
  flex: 1;
  font-weight: 500;
  color: #333;
}

.sc-type {
  font-size: 12px;
  color: #777;
  padding: 2px 8px;
  background: rgba(255, 240, 245, 0.5);
  border-radius: 6px;
  border: 1px solid rgba(220, 210, 218, 0.35);
}

.sc-actions {
  display: flex;
  gap: 6px;
}

/* Toast */
.toast {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%) translateY(-20px);
  background: rgba(255, 255, 255, 0.9);
  padding: 14px 24px;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s;
  z-index: 2000;
}

.toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.toast.success {
  border-left: 4px solid #51CF66;
}

.toast.error {
  border-left: 4px solid #FF6B6B;
}
</style>
