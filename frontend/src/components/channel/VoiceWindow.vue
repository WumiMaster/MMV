<template>
  <!-- 语音频道窗口 -->
  <div class="voice-window" @click="unlockAudio">
    <div class="voice-header">
      <div class="voice-title">
        <svg class="voice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
        {{ subChannelName }}
      </div>
      <button class="leave-btn" @click="leaveVoice" title="退出语音">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
      </button>
    </div>

    <!-- 用户列表 -->
    <div class="voice-users">
      <div
        v-for="user in voiceUsers"
        :key="user.user_id"
        class="voice-user"
        :class="{ speaking: user.is_speaking, muted: user.is_muted }"
      >
        <div class="user-avatar">
          <img v-if="user.avatar" :src="user.avatar" alt="头像" />
          <span v-else>{{ user.nickname?.charAt(0) || '?' }}</span>
          <!-- 说话状态指示器 -->
          <div v-if="user.is_speaking" class="speaking-ring"></div>
          <!-- 闭麦图标 -->
          <div v-if="user.is_muted" class="muted-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="1" y1="1" x2="23" y2="23"></line>
              <path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"></path>
              <path d="M17 16.95A7 7 0 0 1 5 12v-2m14 0v2c0 .38-.03.75-.08 1.12"></path>
              <line x1="12" y1="19" x2="12" y2="23"></line>
              <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
          </div>
        </div>
        <div class="user-name">{{ user.nickname }}</div>
      </div>

      <div v-if="voiceUsers.length === 0" class="empty-tip">
        等待其他人加入...
      </div>
    </div>

    <!-- 音频控制栏 -->
    <div class="voice-controls">
      <!-- 闭麦按钮 -->
      <button
        class="control-btn"
        :class="{ active: isMuted }"
        @click="toggleMute"
        :title="isMuted ? '取消闭麦' : '闭麦'"
      >
        <svg v-if="!isMuted" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="1" y1="1" x2="23" y2="23"></line>
          <path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"></path>
          <path d="M17 16.95A7 7 0 0 1 5 12v-2m14 0v2c0 .38-.03.75-.08 1.12"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      </button>

      <!-- 本地静音按钮 -->
      <button
        class="control-btn"
        :class="{ active: isDeafened }"
        @click="toggleDeafen"
        :title="isDeafened ? '取消静音' : '本地静音'"
      >
        <svg v-if="!isDeafened" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
          <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
          <line x1="23" y1="9" x2="17" y2="15"></line>
          <line x1="17" y1="9" x2="23" y2="15"></line>
        </svg>
      </button>

      <!-- 音量调节 -->
      <div class="volume-control">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
        </svg>
        <input
          type="range"
          min="0"
          max="100"
          v-model="volume"
          class="volume-slider"
          @input="updateVolume"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 语音频道窗口组件
 * 处理 WebRTC P2P 音频连接、音频控制、说话状态检测
 */

import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const props = defineProps({
  subChannelId: {
    type: Number,
    required: true
  },
  subChannelName: {
    type: String,
    default: '语音频道'
  },
  channelId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['close'])

const authStore = useAuthStore()

// 状态
const voiceUsers = ref([])
const isMuted = ref(false)
const isDeafened = ref(false)
const volume = ref(80)

// WebRTC 相关
let ws = null
let localStream = null
let audioContext = null
let analyser = null
let speakingDetectionTimer = null
let refreshUsersTimer = null
let reconnectTimer = null
let reconnectAttempts = 0
const MAX_RECONNECT_ATTEMPTS = 3

// P2P 连接管理 {user_id: RTCPeerConnection}
const peerConnections = ref({})

// 提示音配置
const NOTIFICATION_SOUNDS = {
  join: { name: '清脆提示', freq: [800, 1000], duration: 0.12, type: 'sine' },
  leave: { name: '轻柔下降', freq: [600, 500, 400, 300], duration: 0.12, type: 'sine' },
  userJoin: { name: '清脆双音', freq: [600, 800], duration: 0.12, type: 'sine' },
  userLeave: { name: '低沉提示', freq: [400, 300], duration: 0.12, type: 'sine' }
}

// 播放提示音（使用独立的 AudioContext 避免冲突）
let notificationAudioContext = null
let isPlayingNotification = false

async function playNotificationSound(type) {
  // 防止重叠播放
  if (isPlayingNotification) return
  isPlayingNotification = true

  try {
    // 每次创建新的 AudioContext 避免与语音的 AudioContext 冲突
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)()

    // 确保音频上下文是运行状态
    if (audioCtx.state === 'suspended') {
      await audioCtx.resume()
    }

    const sound = NOTIFICATION_SOUNDS[type]
    if (!sound) return

    const now = audioCtx.currentTime
    const stepDuration = sound.duration + 0.08

    const promises = sound.freq.map((freq, index) => {
      return new Promise((resolve) => {
        const oscillator = audioCtx.createOscillator()
        const gainNode = audioCtx.createGain()

        oscillator.connect(gainNode)
        gainNode.connect(audioCtx.destination)

        oscillator.type = sound.type
        oscillator.frequency.value = freq

        const startTime = now + (index * stepDuration)
        const endTime = startTime + stepDuration

        gainNode.gain.setValueAtTime(0.3, startTime)
        gainNode.gain.exponentialRampToValueAtTime(0.01, endTime - 0.01)

        oscillator.start(startTime)
        oscillator.stop(endTime)

        oscillator.onended = () => {
          resolve()
        }
      })
    })

    // 等待所有音符播放完成
    await Promise.all(promises)

    // 关闭 AudioContext
    await audioCtx.close()

  } catch (e) {
    console.error('播放提示音失败:', e)
  } finally {
    isPlayingNotification = false
  }
}

// 记录上一次的用户列表（用于检测用户加入/离开）
let previousUserIds = new Set()

// 定期刷新语音房间用户
async function fetchVoiceUsers() {
  try {
    const response = await api.get(`/api/voice/${props.subChannelId}/users`)
    const remoteUsers = response.data.users || []

    // 使用 Map 去重，以 user_id 为键
    const userMap = new Map()

    // 先添加远程用户
    for (const user of remoteUsers) {
      userMap.set(user.user_id, { ...user })
    }

    // 确保当前用户在列表中
    const currentUserId = authStore.user?.id
    if (userMap.has(currentUserId)) {
      // 当前用户已在列表中，合并本地状态
      const existing = userMap.get(currentUserId)
      existing.is_muted = isMuted.value
      existing.is_deafened = isDeafened.value
    } else {
      // 当前用户不在列表中，添加
      userMap.set(currentUserId, {
        user_id: currentUserId,
        nickname: authStore.user?.nickname || '我',
        avatar: authStore.user?.avatar,
        is_muted: isMuted.value,
        is_deafened: isDeafened.value,
        is_speaking: false
      })
    }

    // 转换为数组
    const newUserIds = new Set(userMap.keys())

    // 检测其他用户的加入和离开（排除当前用户）
    if (previousUserIds.size > 0) {
      // 检测新加入的用户
      for (const userId of newUserIds) {
        if (userId !== currentUserId && !previousUserIds.has(userId)) {
          playNotificationSound('userJoin')
          break
        }
      }

      // 检测离开的用户
      for (const userId of previousUserIds) {
        if (userId !== currentUserId && !newUserIds.has(userId)) {
          playNotificationSound('userLeave')
          break
        }
      }
    }

    // 更新用户列表和记录
    voiceUsers.value = Array.from(userMap.values())
    previousUserIds = newUserIds

  } catch (error) {
    console.error('获取语音用户失败:', error)
    // 即使API失败，也显示当前用户
    if (voiceUsers.value.length === 0) {
      voiceUsers.value = [{
        user_id: authStore.user?.id,
        nickname: authStore.user?.nickname || '我',
        avatar: authStore.user?.avatar,
        is_muted: isMuted.value,
        is_deafened: isDeafened.value,
        is_speaking: false
      }]
    }
  }
}

function startRefreshingUsers() {
  fetchVoiceUsers()
  refreshUsersTimer = setInterval(fetchVoiceUsers, 2000) // 每2秒刷新
}

// 网络速度监控
let lastBytesSent = 0
let lastBytesReceived = 0
let lastStatsTime = 0
let networkStatsTimer = null

async function updateNetworkStats() {
  const connections = Object.values(peerConnections.value)
  if (connections.length === 0) return

  let totalBytesSent = 0
  let totalBytesReceived = 0
  let now = Date.now()

  for (const conn of connections) {
    if (conn.pc && conn.pc.connectionState === 'connected') {
      try {
        const stats = await conn.pc.getStats()
        stats.forEach(report => {
          if (report.type === 'transport') {
            totalBytesSent += report.bytesSent || 0
            totalBytesReceived += report.bytesReceived || 0
          }
        })
      } catch (e) {
        // 忽略错误
      }
    }
  }

  // 计算速度
  if (lastStatsTime > 0 && now > lastStatsTime) {
    const timeDiff = (now - lastStatsTime) / 1000
    const sentDiff = totalBytesSent - lastBytesSent
    const receivedDiff = totalBytesReceived - lastBytesReceived

    if (timeDiff > 0) {
      // 更新全局状态
      window.__networkStats = {
        uploadSpeed: sentDiff / timeDiff,
        downloadSpeed: receivedDiff / timeDiff
      }
    }
  }

  lastBytesSent = totalBytesSent
  lastBytesReceived = totalBytesReceived
  lastStatsTime = now
}

function startNetworkMonitoring() {
  updateNetworkStats()
  networkStatsTimer = setInterval(updateNetworkStats, 1000)
}

function stopNetworkMonitoring() {
  if (networkStatsTimer) {
    clearInterval(networkStatsTimer)
    networkStatsTimer = null
  }
  window.__networkStats = { uploadSpeed: 0, downloadSpeed: 0 }
}

// 加入语音房间
async function joinVoice() {
  try {
    // 获取麦克风权限
    localStream = await navigator.mediaDevices.getUserMedia({ audio: true })

    // 创建音频分析器（用于说话检测）
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    // 确保音频上下文是运行状态
    if (audioContext.state === 'suspended') {
      await audioContext.resume()
    }
    const source = audioContext.createMediaStreamSource(localStream)
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 256
    source.connect(analyser)

    // 开始说话检测
    startSpeakingDetection()

    // 连接 WebSocket 信令服务器
    connectSignaling()

    // 开始刷新用户列表（会自动添加当前用户）
    startRefreshingUsers()

    // 开始网络监控
    startNetworkMonitoring()

    // 播放加入提示音
    playNotificationSound('join')

  } catch (error) {
    console.error('获取麦克风失败:', error)
    alert('无法获取麦克风权限，请检查浏览器设置')
  }
}

// 连接信令服务器
function connectSignaling() {
  const token = authStore.token
  // 使用相对路径，通过 Vite 代理连接
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = window.location.host // 包含端口
  const wsUrl = `${protocol}//${host}/ws/voice/${props.subChannelId}?token=${token}`

  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    reconnectAttempts = 0 // 连接成功，重置重连次数
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      handleSignalingMessage(data)
    } catch (e) {
      console.error('解析语音信令消息失败:', e)
    }
  }

  ws.onclose = (event) => {
    // 尝试重连（只有在正常关闭时才重连，错误关闭由 onerror 处理）
    if (event.code === 1000 && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
      reconnectAttempts++
      const delay = 2000 * reconnectAttempts // 2秒、4秒、6秒
      reconnectTimer = setTimeout(() => {
        connectSignaling()
      }, delay)
    }
  }

  ws.onerror = (error) => {
    console.error('语音信令错误:', error)
  }
}

// 处理信令消息
async function handleSignalingMessage(data) {
  switch (data.type) {
    case 'voice_peers':
      // 收到房间内的其他用户，建立 P2P 连接
      for (const peer of data.peers) {
        await createPeerConnection(peer.user_id, true)
      }
      break

    case 'offer':
      // 收到 offer，创建 answer
      await handleOffer(data.from_user_id, data.offer)
      break

    case 'answer':
      // 收到 answer
      await handleAnswer(data.from_user_id, data.answer)
      break

    case 'ice_candidate':
      // 收到 ICE candidate
      await handleIceCandidate(data.from_user_id, data.candidate)
      break

    case 'voice_user_muted':
      // 用户闭麦状态变更
      if (data.sub_channel_id === props.subChannelId) {
        const user = voiceUsers.value.find(u => u.user_id === data.user_id)
        if (user) user.is_muted = data.is_muted
      }
      break

    case 'voice_user_speaking':
      // 用户说话状态变更
      if (data.sub_channel_id === props.subChannelId) {
        const user = voiceUsers.value.find(u => u.user_id === data.user_id)
        if (user) user.is_speaking = data.is_speaking
      }
      break
  }
}

// 创建 P2P 连接
async function createPeerConnection(targetUserId, isInitiator) {
  const config = {
    iceServers: [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' }
    ]
  }

  const pc = new RTCPeerConnection(config)

  // 先保存连接引用
  peerConnections.value[targetUserId] = { pc, audio: null }

  // 添加本地音频流
  if (localStream) {
    const audioTracks = localStream.getAudioTracks()
    audioTracks.forEach(track => {
      pc.addTrack(track, localStream)
    })
  }

  // ICE candidate 事件
  pc.onicecandidate = (event) => {
    if (event.candidate && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'ice_candidate',
        target_user_id: targetUserId,
        candidate: event.candidate
      }))
    }
  }

  // 接收远程音频流
  pc.ontrack = (event) => {
    const remoteAudio = new Audio()
    remoteAudio.srcObject = event.streams[0]
    remoteAudio.volume = volume.value / 100
    remoteAudio.autoplay = true

    // 将音频元素添加到 DOM（某些浏览器需要）
    remoteAudio.style.display = 'none'
    remoteAudio.dataset.userId = targetUserId
    document.body.appendChild(remoteAudio)

    // 尝试播放音频
    const playPromise = remoteAudio.play()
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        // 添加点击事件监听器来解锁音频
        const unlockAudio = () => {
          remoteAudio.play().then(() => {
            document.removeEventListener('click', unlockAudio)
            document.removeEventListener('touchstart', unlockAudio)
          }).catch(() => {})
        }
        document.addEventListener('click', unlockAudio)
        document.addEventListener('touchstart', unlockAudio)
      })
    }

    // 更新引用
    if (peerConnections.value[targetUserId]) {
      peerConnections.value[targetUserId].audio = remoteAudio
    }
  }

  // 连接状态变更
  pc.onconnectionstatechange = () => {
    if (pc.connectionState === 'disconnected' || pc.connectionState === 'failed') {
      closePeerConnection(targetUserId)
    }
  }

  // 如果是发起方，创建 offer
  if (isInitiator) {
    const offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'offer',
        target_user_id: targetUserId,
        offer: offer
      }))
    }
  }

  // 保存连接
  if (!peerConnections.value[targetUserId]) {
    peerConnections.value[targetUserId] = { pc, audio: null }
  } else {
    peerConnections.value[targetUserId].pc = pc
  }

  return pc
}

// 处理 offer
async function handleOffer(fromUserId, offer) {
  const pc = await createPeerConnection(fromUserId, false)
  await pc.setRemoteDescription(new RTCSessionDescription(offer))

  const answer = await pc.createAnswer()
  await pc.setLocalDescription(answer)

  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'answer',
      target_user_id: fromUserId,
      answer: answer
    }))
  }
}

// 处理 answer
async function handleAnswer(fromUserId, answer) {
  const conn = peerConnections.value[fromUserId]
  if (conn && conn.pc) {
    await conn.pc.setRemoteDescription(new RTCSessionDescription(answer))
  }
}

// 处理 ICE candidate
async function handleIceCandidate(fromUserId, candidate) {
  const conn = peerConnections.value[fromUserId]
  if (conn && conn.pc) {
    await conn.pc.addIceCandidate(new RTCIceCandidate(candidate))
  }
}

// 关闭 P2P 连接
function closePeerConnection(userId) {
  const conn = peerConnections.value[userId]
  if (conn) {
    if (conn.pc) conn.pc.close()
    if (conn.audio) {
      conn.audio.pause()
      conn.audio.srcObject = null
      // 从 DOM 中移除音频元素
      if (conn.audio.parentNode) {
        conn.audio.parentNode.removeChild(conn.audio)
      }
    }
    delete peerConnections.value[userId]
  }
}

// 说话检测
function startSpeakingDetection() {
  if (!analyser) return

  const dataArray = new Uint8Array(analyser.frequencyBinCount)
  let isSpeaking = false

  function checkSpeaking() {
    if (!analyser) return

    analyser.getByteFrequencyData(dataArray)
    const average = dataArray.reduce((a, b) => a + b) / dataArray.length

    // 阈值判断是否在说话
    const threshold = 30
    const newSpeaking = average > threshold

    if (newSpeaking !== isSpeaking) {
      isSpeaking = newSpeaking

      // 更新本地用户的说话状态
      const localUser = voiceUsers.value.find(u => u.user_id === authStore.user?.id)
      if (localUser) {
        localUser.is_speaking = isSpeaking
      }

      // 发送说话状态
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
          type: 'speaking',
          is_speaking: isSpeaking
        }))
      }
    }

    speakingDetectionTimer = requestAnimationFrame(checkSpeaking)
  }

  checkSpeaking()
}

// 切换闭麦
function toggleMute() {
  isMuted.value = !isMuted.value

  // 禁用/启用麦克风
  if (localStream) {
    localStream.getAudioTracks().forEach(track => {
      track.enabled = !isMuted.value
    })
  }

  // 更新本地用户的静音状态
  const localUser = voiceUsers.value.find(u => u.user_id === authStore.user?.id)
  if (localUser) {
    localUser.is_muted = isMuted.value
  }

  // 发送状态
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'mute',
      is_muted: isMuted.value
    }))
  }
}

// 切换本地静音
function toggleDeafen() {
  isDeafened.value = !isDeafened.value

  // 静音/取消静音所有远程音频
  Object.values(peerConnections.value).forEach(conn => {
    if (conn.audio) {
      conn.audio.muted = isDeafened.value
    }
  })
}

// 更新音量
function updateVolume() {
  Object.values(peerConnections.value).forEach(conn => {
    if (conn.audio) {
      conn.audio.volume = volume.value / 100
    }
  })
}

// 退出语音
function leaveVoice() {
  // 播放退出提示音
  playNotificationSound('leave')

  // 清除重连定时器
  if (reconnectTimer) {
    clearTimeout(reconnectTimer)
    reconnectTimer = null
  }

  // 停止说话检测
  if (speakingDetectionTimer) {
    cancelAnimationFrame(speakingDetectionTimer)
  }

  // 停止刷新用户列表
  if (refreshUsersTimer) {
    clearInterval(refreshUsersTimer)
  }

  // 停止网络监控
  stopNetworkMonitoring()

  // 关闭所有 P2P 连接
  Object.keys(peerConnections.value).forEach(userId => {
    closePeerConnection(userId)
  })

  // 移除所有远程音频元素
  document.querySelectorAll('audio[data-user-id]').forEach(el => {
    el.pause()
    el.srcObject = null
    if (el.parentNode) {
      el.parentNode.removeChild(el)
    }
  })

  // 停止本地音频流
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop())
    localStream = null
  }

  // 关闭音频上下文
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }

  // 清空用户记录
  previousUserIds.clear()

  // 关闭 WebSocket
  if (ws) {
    ws.close()
    ws = null
  }

  emit('close')
}

// 解锁音频播放（需要用户交互）
function unlockAudio() {
  // 恢复音频上下文
  if (audioContext && audioContext.state === 'suspended') {
    audioContext.resume()
  }
  if (notificationAudioContext && notificationAudioContext.state === 'suspended') {
    notificationAudioContext.resume()
  }

  // 尝试播放所有远程音频
  Object.values(peerConnections.value).forEach(conn => {
    if (conn.audio && conn.audio.paused) {
      conn.audio.play().catch(() => {})
    }
  })
}

// 页面关闭时清理资源
function handleBeforeUnload() {
  leaveVoice()
}

// 组件挂载时加入语音
onMounted(() => {
  joinVoice()
  // 监听页面关闭事件
  window.addEventListener('beforeunload', handleBeforeUnload)
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
  leaveVoice()
})

// 暴露给父组件
defineExpose({
  localStream
})
</script>

<style scoped>
.voice-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  background: linear-gradient(180deg, rgba(255, 240, 248, 0.5) 0%, rgba(255, 245, 250, 0.4) 100%);
  overflow: hidden;
  box-sizing: border-box;
}

.voice-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid rgba(220, 200, 210, 0.4);
  background: rgba(255, 242, 250, 0.4);
  flex-shrink: 0;
}

.voice-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.voice-icon {
  width: 18px;
  height: 18px;
  color: #FF9EB5;
}

.leave-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 107, 107, 0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.leave-btn:hover {
  background: rgba(255, 107, 107, 0.25);
}

.leave-btn svg {
  width: 16px;
  height: 16px;
  color: #FF6B6B;
}

.voice-users {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 8px 10px;
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
  align-items: center;
  min-height: 0;
  scrollbar-width: thin;
}

.voice-users::-webkit-scrollbar {
  height: 4px;
}

.voice-users::-webkit-scrollbar-thumb {
  background: rgba(255, 170, 195, 0.4);
  border-radius: 2px;
}

.voice-users::-webkit-scrollbar-track {
  background: transparent;
}

.voice-user {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  width: 64px;
  padding: 0;
  margin: 0;
  min-height: 0;
  flex-shrink: 0;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: transform 0.2s ease;
}

.voice-user.speaking .user-avatar {
  transform: scale(1.1);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.user-avatar span {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.speaking-ring {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border-radius: 50%;
  border: 3px solid #7ED7A7;
  animation: speakingPulse 1s ease-in-out infinite;
}

@keyframes speakingPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; }
}

.muted-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #FF6B6B;
  display: flex;
  align-items: center;
  justify-content: center;
}

.muted-badge svg {
  width: 12px;
  height: 12px;
  color: white;
}

.user-name {
  font-size: 12px;
  color: #666;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 64px;
  margin: 0;
  padding: 0;
  line-height: 1.2;
  min-height: 0;
}

.empty-tip {
  width: 100%;
  text-align: center;
  color: #999;
  padding: 8px 0;
  font-size: 14px;
}

.voice-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 6px 12px;
  border-top: 1px solid rgba(220, 200, 210, 0.4);
  background: rgba(255, 242, 250, 0.4);
  flex-shrink: 0;
}

.control-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 240, 248, 0.6);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.control-btn:hover {
  background: rgba(255, 230, 240, 0.8);
}

.control-btn.active {
  background: rgba(255, 107, 107, 0.2);
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.control-btn svg {
  width: 16px;
  height: 16px;
  color: #666;
}

.control-btn.active svg {
  color: #FF6B6B;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 8px;
}

.volume-control svg {
  width: 16px;
  height: 16px;
  color: #888;
}

.volume-slider {
  width: 80px;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(200, 190, 198, 0.4);
  border-radius: 2px;
  outline: none;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9EB5, #7ED7A7);
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 响应式样式 */
@media (max-width: 768px) {
  .voice-header {
    padding: 6px 10px;
  }

  .voice-title {
    font-size: 13px;
    gap: 6px;
  }

  .voice-icon {
    width: 16px;
    height: 16px;
  }

  .leave-btn {
    width: 28px;
    height: 28px;
    border-radius: 6px;
  }

  .leave-btn svg {
    width: 14px;
    height: 14px;
  }

  .voice-users {
    padding: 6px 8px;
    gap: 8px;
  }

  .voice-user {
    width: 52px;
    gap: 3px;
  }

  .user-avatar {
    width: 40px;
    height: 40px;
  }

  .user-avatar span {
    font-size: 15px;
  }

  .user-name {
    font-size: 11px;
    max-width: 52px;
  }

  .voice-controls {
    padding: 5px 10px;
    gap: 8px;
  }

  .control-btn {
    width: 28px;
    height: 28px;
    border-radius: 6px;
  }

  .control-btn svg {
    width: 14px;
    height: 14px;
  }

  .volume-control {
    gap: 4px;
    padding: 0 6px;
  }

  .volume-control svg {
    width: 14px;
    height: 14px;
  }

  .volume-slider {
    width: 60px;
    height: 3px;
  }

  .volume-slider::-webkit-slider-thumb {
    width: 12px;
    height: 12px;
  }
}

@media (max-width: 480px) {
  .voice-header {
    padding: 5px 8px;
  }

  .voice-title {
    font-size: 12px;
    gap: 4px;
  }

  .voice-icon {
    width: 14px;
    height: 14px;
  }

  .leave-btn {
    width: 26px;
    height: 26px;
    border-radius: 6px;
  }

  .leave-btn svg {
    width: 12px;
    height: 12px;
  }

  .voice-users {
    padding: 4px 6px;
    gap: 6px;
  }

  .voice-user {
    width: 46px;
    gap: 2px;
  }

  .user-avatar {
    width: 36px;
    height: 36px;
  }

  .user-avatar span {
    font-size: 13px;
  }

  .user-name {
    font-size: 10px;
    max-width: 46px;
  }

  .voice-controls {
    padding: 4px 8px;
    gap: 6px;
  }

  .control-btn {
    width: 26px;
    height: 26px;
    border-radius: 6px;
  }

  .control-btn svg {
    width: 12px;
    height: 12px;
  }

  .volume-control {
    gap: 3px;
    padding: 0 4px;
  }

  .volume-control svg {
    width: 12px;
    height: 12px;
  }

  .volume-slider {
    width: 50px;
    height: 3px;
  }

  .volume-slider::-webkit-slider-thumb {
    width: 10px;
    height: 10px;
  }
}
</style>
