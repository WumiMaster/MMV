<template>
  <div class="admin-container">
    <!-- 顶部导航栏 -->
    <nav class="top-navbar">
      <div class="nav-left">
        <div class="logo">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
        </div>
        <div class="channel-info">
          <div class="channel-name">管理员后台</div>
          <div class="channel-id">系统管理面板</div>
        </div>
      </div>
      <div class="nav-right">
        <button class="icon-btn" title="返回频道" @click="goToChannel">
          <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
          </svg>
        </button>
        <button class="icon-btn" title="退出登录" @click="handleLogout">
          <svg class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>
    </nav>

    <!-- Tab 标签 -->
    <div class="tab-bar">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'users' }"
        @click="activeTab = 'users'"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
        用户管理
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'channels' }"
        @click="activeTab = 'channels'"
      >
        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
          <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
          <line x1="6" y1="6" x2="6.01" y2="6"></line>
          <line x1="6" y1="18" x2="6.01" y2="18"></line>
        </svg>
        频道管理
      </button>
    </div>

    <!-- 主要内容 -->
    <div class="admin-content">
      <!-- 用户管理 -->
      <div v-if="activeTab === 'users'" class="glass-card admin-card animate-slide-up">
        <div class="admin-header">
          <div class="admin-title">用户管理</div>
          <button class="btn-green" @click="showCreateModal = true">
            + 新增用户
          </button>
        </div>

        <!-- 用户列表 -->
        <div class="user-table-container">
          <table class="user-table">
            <thead>
              <tr>
                <th>头像</th>
                <th>用户名</th>
                <th>昵称</th>
                <th>角色</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>
                  <div class="user-avatar">
                    <img v-if="user.avatar" :src="user.avatar" alt="头像" />
                    <span v-else>{{ user.nickname.charAt(0) }}</span>
                  </div>
                </td>
                <td>{{ user.username }}</td>
                <td>{{ user.nickname }}</td>
                <td>
                  <span class="role-badge" :class="user.role === 'admin' ? 'role-admin' : 'role-user'">
                    {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                  </span>
                </td>
                <td>
                  <div class="action-btns">
                    <button class="btn-edit" @click="editUser(user)">编辑</button>
                    <button class="btn-delete" @click="confirmDeleteUser(user)">删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 分页 -->
        <div class="pagination">
          <button :disabled="currentPage <= 1" @click="loadUsers(currentPage - 1)">上一页</button>
          <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
          <button :disabled="currentPage >= totalPages" @click="loadUsers(currentPage + 1)">下一页</button>
        </div>
      </div>

      <!-- 频道管理 -->
      <div v-if="activeTab === 'channels'" class="glass-card admin-card animate-slide-up">
        <ChannelManage />
      </div>
    </div>

    <!-- 创建用户弹窗 -->
    <Teleport to="body">
      <div v-if="showCreateModal" class="modal-overlay animate-overlay-in" @click.self="showCreateModal = false">
        <div class="glass-card modal animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">新增用户</div>
            <button class="modal-close" @click="showCreateModal = false">×</button>
          </div>

        <!-- 头像上传 -->
        <div class="avatar-upload" @click="triggerCreateAvatarInput">
          <div v-if="createAvatarPreview" class="avatar-preview">
            <img :src="createAvatarPreview" alt="头像预览" />
          </div>
          <div v-else class="avatar-placeholder">
            <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
              <circle cx="12" cy="13" r="4"></circle>
            </svg>
            <div>点击上传头像</div>
          </div>
          <input ref="createAvatarInput" type="file" accept="image/*" style="display: none" @change="handleCreateAvatarChange" />
        </div>

        <div class="form-group">
          <label class="form-label">用户名 *</label>
          <input v-model="createForm.username" type="text" class="glass-input" placeholder="请输入用户名" />
        </div>

        <div class="form-group">
          <label class="form-label">密码 *</label>
          <input v-model="createForm.password" type="password" class="glass-input" placeholder="请输入密码" />
        </div>

        <div class="form-group">
          <label class="form-label">昵称 *</label>
          <input v-model="createForm.nickname" type="text" class="glass-input" placeholder="对外显示的昵称" />
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="showCreateModal = false">取消</button>
          <button class="btn-primary" @click="handleCreateUser">确认</button>
        </div>
      </div>
      </div>
    </Teleport>

    <!-- 编辑用户弹窗 -->
    <Teleport to="body">
      <div v-if="showEditModal" class="modal-overlay animate-overlay-in" @click.self="showEditModal = false">
        <div class="glass-card modal animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">编辑用户</div>
            <button class="modal-close" @click="showEditModal = false">×</button>
        </div>

        <div class="form-group">
          <label class="form-label">昵称</label>
          <input v-model="editForm.nickname" type="text" class="glass-input" placeholder="对外显示的昵称" />
        </div>

        <div class="form-group">
          <label class="form-label">新密码（留空则不修改）</label>
          <input v-model="editForm.password" type="password" class="glass-input" placeholder="请输入新密码" />
        </div>

        <div class="form-group">
          <label class="form-label">角色</label>
          <select v-model="editForm.role" class="glass-input">
            <option value="user">普通用户</option>
            <option value="admin">管理员</option>
          </select>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="showEditModal = false">取消</button>
          <button class="btn-primary" @click="handleUpdateUser">确认</button>
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
          确定要删除用户 <strong>{{ deleteTarget?.nickname }}</strong> 吗？<br />
          此操作不可撤销。
        </p>

        <div class="modal-footer">
          <button class="btn-cancel" @click="showDeleteModal = false">取消</button>
          <button class="btn-danger" @click="handleDeleteUser">确认删除</button>
        </div>
      </div>
      </div>
    </Teleport>

    <!-- 不能删除自己的提示弹窗 -->
    <Teleport to="body">
      <div v-if="showCannotDeleteSelfModal" class="modal-overlay animate-overlay-in" @click.self="showCannotDeleteSelfModal = false">
        <div class="glass-card modal animate-modal-in">
          <div class="modal-header">
            <div class="modal-title">⚠️ 提示</div>
            <button class="modal-close" @click="showCannotDeleteSelfModal = false">×</button>
        </div>

        <p class="modal-desc">
          不能删除当前登录的管理员账号！<br />
          如需删除，请使用其他管理员账号登录后操作。
        </p>

        <div class="modal-footer">
          <button class="btn-primary" @click="showCannotDeleteSelfModal = false">我知道了</button>
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
 * 管理员后台页面
 * 包含用户管理和频道管理两个 Tab
 */

import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'
import ChannelManage from './ChannelManage.vue'

const router = useRouter()
const authStore = useAuthStore()

// 当前 Tab
const activeTab = ref('users')

// 用户列表
const users = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalUsers = ref(0)
const totalPages = computed(() => Math.ceil(totalUsers.value / pageSize.value))

// 弹窗状态
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showCannotDeleteSelfModal = ref(false)

// 表单数据
const createForm = ref({ username: '', password: '', nickname: '' })
const editForm = ref({ id: null, nickname: '', password: '', role: 'user' })
const deleteTarget = ref(null)

// 头像上传
const createAvatarInput = ref(null)
const createAvatarPreview = ref(null)
const createAvatarFile = ref(null)

// Toast 提示
const toast = ref({ show: false, message: '', type: 'success' })

function showToast(message, type = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => { toast.value.show = false }, 2000)
}

// 加载用户列表
async function loadUsers(page = 1) {
  try {
    const response = await api.get('/api/admin/users', {
      params: { page, page_size: pageSize.value }
    })
    users.value = response.data.users
    totalUsers.value = response.data.total
    currentPage.value = page
  } catch (error) {
    showToast('加载用户列表失败', 'error')
  }
}

// 触发头像选择
function triggerCreateAvatarInput() {
  createAvatarInput.value.click()
}

// 处理头像选择
function handleCreateAvatarChange(event) {
  const file = event.target.files[0]
  if (!file) return
  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    showToast('图片大小不能超过 5MB', 'error')
    return
  }
  createAvatarFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => { createAvatarPreview.value = e.target.result }
  reader.readAsDataURL(file)
}

// 创建用户
async function handleCreateUser() {
  if (!createForm.value.username || !createForm.value.password || !createForm.value.nickname) {
    showToast('请填写所有必填项', 'error')
    return
  }
  try {
    const response = await api.post('/api/admin/users', createForm.value)
    const newUser = response.data
    if (createAvatarFile.value) {
      const formData = new FormData()
      formData.append('file', createAvatarFile.value)
      await api.post(`/api/admin/users/${newUser.id}/avatar`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    showToast('用户创建成功')
    showCreateModal.value = false
    createForm.value = { username: '', password: '', nickname: '' }
    createAvatarPreview.value = null
    createAvatarFile.value = null
    loadUsers(currentPage.value)
  } catch (error) {
    showToast(error.response?.data?.detail || '创建失败', 'error')
  }
}

// 编辑用户
function editUser(user) {
  editForm.value = { id: user.id, nickname: user.nickname, password: '', role: user.role }
  showEditModal.value = true
}

// 更新用户
async function handleUpdateUser() {
  try {
    const updateData = { nickname: editForm.value.nickname, role: editForm.value.role }
    if (editForm.value.password) updateData.password = editForm.value.password
    await api.put(`/api/admin/users/${editForm.value.id}`, updateData)
    showToast('用户信息已更新')
    showEditModal.value = false
    loadUsers(currentPage.value)
  } catch (error) {
    showToast(error.response?.data?.detail || '更新失败', 'error')
  }
}

// 确认删除用户
function confirmDeleteUser(user) {
  if (user.username === authStore.user?.username) {
    showCannotDeleteSelfModal.value = true
    return
  }
  deleteTarget.value = user
  showDeleteModal.value = true
}

// 删除用户
async function handleDeleteUser() {
  try {
    await api.delete(`/api/admin/users/${deleteTarget.value.id}`)
    showToast('用户已删除')
    showDeleteModal.value = false
    loadUsers(currentPage.value)
  } catch (error) {
    showToast(error.response?.data?.detail || '删除失败', 'error')
  }
}

// 返回频道页
function goToChannel() {
  router.push('/channel')
}

// 退出登录
function handleLogout() {
  authStore.logout()
  router.push('/login')
}

// 页面加载
onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  position: relative;
  isolation: isolate;
}

/* 顶部导航栏 */
.top-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.tab-icon {
  width: 18px;
  height: 18px;
  vertical-align: middle;
  margin-right: 6px;
}

.upload-icon {
  width: 32px;
  height: 32px;
  color: #999;
  margin-bottom: 8px;
}

.channel-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.channel-name {
  font-weight: 600;
  font-size: 15px;
}

.channel-id {
  font-size: 12px;
  color: #666;
}

.nav-right {
  display: flex;
  gap: 10px;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  font-size: 18px;
}

.icon-btn:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.8);
}

.icon-svg {
  width: 20px;
  height: 20px;
}

/* Tab 标签 */
.tab-bar {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  height: 48px;
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  padding: 0 24px;
  z-index: 99;
}

.tab-btn {
  padding: 0 20px;
  height: 100%;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  position: relative;
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-btn:hover {
  color: #333;
}

.tab-btn.active {
  color: #FF9EB5;
  font-weight: 600;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20px;
  right: 20px;
  height: 3px;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  border-radius: 3px 3px 0 0;
}

/* 主要内容 */
.admin-content {
  padding-top: 132px;
  max-width: 1200px;
  margin: 0 auto;
  padding-left: 20px;
  padding-right: 20px;
  padding-bottom: 20px;
}

.admin-card {
  padding: 24px;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.admin-title {
  font-size: 18px;
  font-weight: 700;
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

/* 用户表格 */
.user-table-container {
  overflow-x: auto;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th,
.user-table td {
  padding: 14px 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}

.user-table th {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
}

.user-table tr:hover td {
  background: rgba(255, 255, 255, 0.3);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  font-weight: 600;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.role-admin {
  background: rgba(255, 158, 181, 0.2);
  color: #d63384;
}

.role-user {
  background: rgba(126, 215, 167, 0.2);
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
  transition: all 0.15s;
}

.btn-edit:hover {
  background: #7ED7A7;
  color: white;
}

.btn-delete {
  padding: 6px 14px;
  border: none;
  background: transparent;
  color: #FF6B6B;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.15s;
}

.btn-delete:hover {
  background: rgba(255, 107, 107, 0.1);
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s;
}

.pagination button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.8);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 弹窗样式 */
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
  margin: 0;
  padding: 0;
}

.modal {
  width: 90%;
  max-width: 440px;
  padding: 28px;
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

.avatar-upload {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px dashed rgba(200, 190, 198, 0.6);
  background: rgba(255, 245, 250, 0.5);
  margin: 0 auto 24px;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
}

.avatar-upload:hover {
  border-color: #7ED7A7;
  background: rgba(255, 240, 248, 0.7);
  transform: scale(1.05);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 12px;
}

.avatar-placeholder .upload-icon {
  width: 28px;
  height: 28px;
  color: #999;
  margin-bottom: 4px;
}

.avatar-preview {
  width: 100%;
  height: 100%;
}

.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.modal-footer {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 220, 230, 0.4);
}

.modal-footer .btn-primary,
.modal-footer .btn-cancel {
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

.btn-cancel {
  height: 44px;
  border: 1px solid rgba(200, 190, 198, 0.5);
  background: rgba(255, 245, 250, 0.6);
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease, border-color 0.2s ease;
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

/* Toast 提示 */
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
