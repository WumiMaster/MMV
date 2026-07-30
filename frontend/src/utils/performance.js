/**
 * 性能优化工具
 * 提供动画性能优化相关的工具函数
 */

/**
 * 检查是否支持硬件加速
 * @returns {boolean} - 是否支持
 */
export function supportsHardwareAcceleration() {
  const canvas = document.createElement('canvas')
  const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
  return !!gl
}

/**
 * 启用硬件加速
 * @param {HTMLElement} element - 目标元素
 */
export function enableHardwareAcceleration(element) {
  element.style.transform = 'translateZ(0)'
  element.style.backfaceVisibility = 'hidden'
  element.style.perspective = '1000px'
}

/**
 * 禁用硬件加速
 * @param {HTMLElement} element - 目标元素
 */
export function disableHardwareAcceleration(element) {
  element.style.transform = ''
  element.style.backfaceVisibility = ''
  element.style.perspective = ''
}

/**
 * 设置 will-change 属性
 * @param {HTMLElement} element - 目标元素
 * @param {string} properties - 属性列表
 */
export function setWillChange(element, properties) {
  element.style.willChange = properties
}

/**
 * 清除 will-change 属性
 * @param {HTMLElement} element - 目标元素
 */
export function clearWillChange(element) {
  element.style.willChange = ''
}

/**
 * 使用 requestAnimationFrame 优化动画
 * @param {Function} callback - 回调函数
 * @returns {number} - 动画帧 ID
 */
export function optimizedRAF(callback) {
  return requestAnimationFrame(callback)
}

/**
 * 批量 DOM 操作优化
 * @param {Function} operations - 操作函数
 */
export function batchDOMOperations(operations) {
  // 读取操作
  const reads = []
  const writes = []

  // 分离读写操作
  operations({
    read: (fn) => reads.push(fn),
    write: (fn) => writes.push(fn)
  })

  // 执行读操作
  reads.forEach(fn => fn())

  // 执行写操作
  requestAnimationFrame(() => {
    writes.forEach(fn => fn())
  })
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} wait - 等待时间
 * @param {boolean} immediate - 是否立即执行
 * @returns {Function} - 防抖后的函数
 */
export function debounce(func, wait, immediate = false) {
  let timeout = null

  return function executedFunction(...args) {
    const context = this

    const later = () => {
      timeout = null
      if (!immediate) func.apply(context, args)
    }

    const callNow = immediate && !timeout

    clearTimeout(timeout)
    timeout = setTimeout(later, wait)

    if (callNow) func.apply(context, args)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} limit - 限制时间
 * @returns {Function} - 节流后的函数
 */
export function throttle(func, limit) {
  let inThrottle = false
  let lastResult = null

  return function executedFunction(...args) {
    const context = this

    if (!inThrottle) {
      lastResult = func.apply(context, args)
      inThrottle = true

      setTimeout(() => {
        inThrottle = false
      }, limit)
    }

    return lastResult
  }
}

/**
 * 测量动画性能
 * @param {Function} animationFunction - 动画函数
 * @param {number} iterations - 迭代次数
 * @returns {Object} - 性能指标
 */
export async function measureAnimationPerformance(animationFunction, iterations = 100) {
  const times = []
  const fps = []

  for (let i = 0; i < iterations; i++) {
    const startTime = performance.now()
    const startFrame = performance.now()

    await animationFunction()

    const endTime = performance.now()
    const endFrame = performance.now()

    times.push(endTime - startTime)
    fps.push(1000 / (endFrame - startFrame))
  }

  const avgTime = times.reduce((a, b) => a + b, 0) / times.length
  const avgFps = fps.reduce((a, b) => a + b, 0) / fps.length
  const minTime = Math.min(...times)
  const maxTime = Math.max(...times)

  return {
    averageTime: avgTime,
    averageFps: avgFps,
    minTime,
    maxTime,
    iterations
  }
}

/**
 * 优化图片加载
 * @param {string} src - 图片地址
 * @param {Object} options - 选项
 * @returns {Promise} - 加载完成的 Promise
 */
export function optimizedImageLoad(src, options = {}) {
  const {
    width,
    height,
    quality = 0.8,
    format = 'webp'
  } = options

  return new Promise((resolve, reject) => {
    const img = new Image()

    img.onload = () => {
      // 如果需要调整大小
      if (width || height) {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')

        canvas.width = width || img.width
        canvas.height = height || img.height

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height)

        canvas.toBlob(
          (blob) => {
            resolve({
              original: img,
              optimized: URL.createObjectURL(blob),
              width: canvas.width,
              height: canvas.height
            })
          },
          `image/${format}`,
          quality
        )
      } else {
        resolve({
          original: img,
          optimized: src,
          width: img.width,
          height: img.height
        })
      }
    }

    img.onerror = reject
    img.src = src
  })
}

/**
 * 创建动画队列
 * @param {number} concurrency - 并发数
 * @returns {Object} - 队列控制对象
 */
export function createAnimationQueue(concurrency = 1) {
  const queue = []
  let running = 0

  function add(animation) {
    return new Promise((resolve, reject) => {
      queue.push({
        animation,
        resolve,
        reject
      })

      processQueue()
    })
  }

  async function processQueue() {
    if (running >= concurrency || queue.length === 0) {
      return
    }

    running++
    const { animation, resolve, reject } = queue.shift()

    try {
      const result = await animation()
      resolve(result)
    } catch (error) {
      reject(error)
    } finally {
      running--
      processQueue()
    }
  }

  function clear() {
    queue.length = 0
  }

  return {
    add,
    clear,
    get queueLength() {
      return queue.length
    },
    get running() {
      return running
    }
  }
}

/**
 * 优化滚动性能
 * @param {HTMLElement} element - 目标元素
 * @param {Function} callback - 回调函数
 * @returns {Function} - 清理函数
 */
export function optimizedScroll(element, callback) {
  let ticking = false

  function onScroll() {
    if (!ticking) {
      requestAnimationFrame(() => {
        callback()
        ticking = false
      })
      ticking = true
    }
  }

  element.addEventListener('scroll', onScroll, { passive: true })

  return () => {
    element.removeEventListener('scroll', onScroll)
  }
}

/**
 * 优化 ResizeObserver
 * @param {HTMLElement} element - 目标元素
 * @param {Function} callback - 回调函数
 * @returns {Object} - 观察器控制对象
 */
export function optimizedResizeObserver(element, callback) {
  let animationFrame = null

  const observer = new ResizeObserver((entries) => {
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
    }

    animationFrame = requestAnimationFrame(() => {
      callback(entries)
    })
  })

  observer.observe(element)

  return {
    disconnect: () => {
      if (animationFrame) {
        cancelAnimationFrame(animationFrame)
      }
      observer.disconnect()
    }
  }
}

/**
 * 优化 IntersectionObserver
 * @param {HTMLElement} element - 目标元素
 * @param {Function} callback - 回调函数
 * @param {Object} options - 选项
 * @returns {Object} - 观察器控制对象
 */
export function optimizedIntersectionObserver(element, callback, options = {}) {
  const {
    threshold = 0.1,
    rootMargin = '0px',
    once = false
  } = options

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          callback(entry)
          if (once) {
            observer.unobserve(entry.target)
          }
        }
      })
    },
    { threshold, rootMargin }
  )

  observer.observe(element)

  return {
    disconnect: () => observer.disconnect(),
    unobserve: () => observer.unobserve(element)
  }
}

/**
 * 创建动画性能监控
 * @returns {Object} - 监控控制对象
 */
export function createPerformanceMonitor() {
  const metrics = {
    fps: [],
    frameTimes: [],
    longTasks: []
  }

  let frameCount = 0
  let lastTime = performance.now()
  let animationFrame = null

  function monitor() {
    const currentTime = performance.now()
    const deltaTime = currentTime - lastTime

    frameCount++
    metrics.frameTimes.push(deltaTime)

    // 计算 FPS
    if (deltaTime >= 1000) {
      metrics.fps.push(frameCount)
      frameCount = 0
      lastTime = currentTime
    }

    // 检测长任务
    if (deltaTime > 50) {
      metrics.longTasks.push({
        timestamp: currentTime,
        duration: deltaTime
      })
    }

    animationFrame = requestAnimationFrame(monitor)
  }

  function start() {
    lastTime = performance.now()
    monitor()
  }

  function stop() {
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
    }
  }

  function getMetrics() {
    const avgFps = metrics.fps.length > 0
      ? metrics.fps.reduce((a, b) => a + b, 0) / metrics.fps.length
      : 0

    const avgFrameTime = metrics.frameTimes.length > 0
      ? metrics.frameTimes.reduce((a, b) => a + b, 0) / metrics.frameTimes.length
      : 0

    return {
      averageFps: Math.round(avgFps),
      averageFrameTime: Math.round(avgFrameTime * 100) / 100,
      longTaskCount: metrics.longTasks.length,
      longTasks: metrics.longTasks.slice(-10) // 最近 10 个长任务
    }
  }

  function reset() {
    metrics.fps = []
    metrics.frameTimes = []
    metrics.longTasks = []
    frameCount = 0
    lastTime = performance.now()
  }

  return {
    start,
    stop,
    getMetrics,
    reset
  }
}

/**
 * 优化动画帧率
 * @param {Function} callback - 回调函数
 * @param {number} targetFps - 目标帧率
 * @returns {Object} - 控制对象
 */
export function optimizeFrameRate(callback, targetFps = 60) {
  const interval = 1000 / targetFps
  let lastTime = 0
  let animationFrame = null
  let isRunning = false

  function tick(currentTime) {
    if (!isRunning) return

    const deltaTime = currentTime - lastTime

    if (deltaTime >= interval) {
      callback(deltaTime)
      lastTime = currentTime - (deltaTime % interval)
    }

    animationFrame = requestAnimationFrame(tick)
  }

  function start() {
    if (isRunning) return

    isRunning = true
    lastTime = performance.now()
    animationFrame = requestAnimationFrame(tick)
  }

  function stop() {
    isRunning = false
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
      animationFrame = null
    }
  }

  return {
    start,
    stop,
    get isRunning() {
      return isRunning
    }
  }
}

// 导出所有工具
export default {
  supportsHardwareAcceleration,
  enableHardwareAcceleration,
  disableHardwareAcceleration,
  setWillChange,
  clearWillChange,
  optimizedRAF,
  batchDOMOperations,
  debounce,
  throttle,
  measureAnimationPerformance,
  optimizedImageLoad,
  createAnimationQueue,
  optimizedScroll,
  optimizedResizeObserver,
  optimizedIntersectionObserver,
  createPerformanceMonitor,
  optimizeFrameRate
}
