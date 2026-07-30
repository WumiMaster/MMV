/**
 * 动画工具函数
 * 提供动画相关的工具方法和辅助函数
 */

/**
 * 创建动画序列
 * @param {Array} animations - 动画配置数组
 * @returns {Promise} - 动画完成的Promise
 */
export function createAnimationSequence(animations) {
  return animations.reduce((promise, animation) => {
    return promise.then(() => {
      return new Promise((resolve) => {
        if (typeof animation === 'function') {
          animation()
          setTimeout(resolve, 300)
        } else if (animation.element && animation.keyframes) {
          const anim = animation.element.animate(animation.keyframes, animation.options || {})
          anim.onfinish = resolve
        } else {
          setTimeout(resolve, animation.duration || 300)
        }
      })
    })
  }, Promise.resolve())
}

/**
 * 创建交错动画
 * @param {Array} elements - 元素数组
 * @param {Object} animation - 动画配置
 * @param {number} staggerDelay - 交错延迟
 */
export function createStaggerAnimation(elements, animation, staggerDelay = 50) {
  elements.forEach((element, index) => {
    setTimeout(() => {
      if (element && element.animate) {
        element.animate(animation.keyframes, {
          duration: animation.duration || 300,
          easing: animation.easing || 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
          fill: 'forwards'
        })
      }
    }, index * staggerDelay)
  })
}

/**
 * 创建弹性动画
 * @param {HTMLElement} element - 目标元素
 * @param {Object} options - 配置选项
 * @returns {Animation} - 动画对象
 */
export function createSpringAnimation(element, options = {}) {
  const {
    property = 'transform',
    from = 0,
    to = 1,
    stiffness = 100,
    damping = 10,
    mass = 1
  } = options

  const keyframes = []
  const steps = 60
  const dt = 1 / 60

  let x = from
  let v = 0

  for (let i = 0; i <= steps; i++) {
    const f = -stiffness * (x - to) - damping * v
    const a = f / mass
    v += a * dt
    x += v * dt

    keyframes.push({
      [property]: x,
      offset: i / steps
    })
  }

  return element.animate(keyframes, {
    duration: options.duration || 1000,
    easing: 'linear',
    fill: 'forwards'
  })
}

/**
 * 创建缓动函数
 * @param {string} type - 缓动类型
 * @returns {Function} - 缓动函数
 */
export function createEasingFunction(type) {
  const easings = {
    linear: (t) => t,
    easeInQuad: (t) => t * t,
    easeOutQuad: (t) => t * (2 - t),
    easeInOutQuad: (t) => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
    easeInCubic: (t) => t * t * t,
    easeOutCubic: (t) => (--t) * t * t + 1,
    easeInOutCubic: (t) => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
    easeInQuart: (t) => t * t * t * t,
    easeOutQuart: (t) => 1 - (--t) * t * t * t,
    easeInOutQuart: (t) => t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t,
    easeInQuint: (t) => t * t * t * t * t,
    easeOutQuint: (t) => 1 + (--t) * t * t * t * t,
    easeInOutQuint: (t) => t < 0.5 ? 16 * t * t * t * t * t : 1 + 16 * (--t) * t * t * t * t,
    easeInSine: (t) => 1 - Math.cos(t * Math.PI / 2),
    easeOutSine: (t) => Math.sin(t * Math.PI / 2),
    easeInOutSine: (t) => -(Math.cos(Math.PI * t) - 1) / 2,
    easeInExpo: (t) => t === 0 ? 0 : Math.pow(2, 10 * (t - 1)),
    easeOutExpo: (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
    easeInOutExpo: (t) => {
      if (t === 0 || t === 1) return t
      if (t < 0.5) return Math.pow(2, 20 * t - 10) / 2
      return (2 - Math.pow(2, -20 * t + 10)) / 2
    },
    easeInCirc: (t) => 1 - Math.sqrt(1 - t * t),
    easeOutCirc: (t) => Math.sqrt(1 - (t - 1) * (t - 1)),
    easeInOutCirc: (t) => {
      if (t < 0.5) return (1 - Math.sqrt(1 - 4 * t * t)) / 2
      return (Math.sqrt(1 - (2 * t - 2) * (2 * t - 2)) + 1) / 2
    },
    easeInBack: (t) => {
      const s = 1.70158
      return t * t * ((s + 1) * t - s)
    },
    easeOutBack: (t) => {
      const s = 1.70158
      t = t - 1
      return t * t * ((s + 1) * t + s) + 1
    },
    easeInOutBack: (t) => {
      const s = 1.70158 * 1.525
      if (t < 0.5) {
        return (t * t * ((s + 1) * t - s)) * 2
      }
      t = t * 2 - 2
      return (t * t * ((s + 1) * t + s) + 2) / 2
    },
    easeInElastic: (t) => {
      if (t === 0 || t === 1) return t
      return -Math.pow(2, 10 * t - 10) * Math.sin((t * 10 - 10.75) * (2 * Math.PI) / 3)
    },
    easeOutElastic: (t) => {
      if (t === 0 || t === 1) return t
      return Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * (2 * Math.PI) / 3) + 1
    },
    easeInOutElastic: (t) => {
      if (t === 0 || t === 1) return t
      if (t < 0.5) {
        return -(Math.pow(2, 20 * t - 10) * Math.sin((20 * t - 11.125) * (2 * Math.PI) / 4.5)) / 2
      }
      return (Math.pow(2, -20 * t + 10) * Math.sin((20 * t - 11.125) * (2 * Math.PI) / 4.5)) / 2 + 1
    },
    easeInBounce: (t) => 1 - easings.easeOutBounce(1 - t),
    easeOutBounce: (t) => {
      const n1 = 7.5625
      const d1 = 2.75
      if (t < 1 / d1) {
        return n1 * t * t
      } else if (t < 2 / d1) {
        t -= 1.5 / d1
        return n1 * t * t + 0.75
      } else if (t < 2.5 / d1) {
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
      } else {
        t -= 2.625 / d1
        return n1 * t * t + 0.984375
      }
    },
    easeInOutBounce: (t) => {
      if (t < 0.5) {
        return (1 - easings.easeOutBounce(1 - 2 * t)) / 2
      }
      return (1 + easings.easeOutBounce(2 * t - 1)) / 2
    }
  }

  return easings[type] || easings.linear
}

/**
 * 创建动画计时器
 * @param {Function} callback - 回调函数
 * @param {number} duration - 持续时间
 * @param {Function} easing - 缓动函数
 * @returns {Object} - 计时器控制对象
 */
export function createAnimationTimer(callback, duration, easing = (t) => t) {
  let startTime = null
  let animationFrame = null
  let isRunning = false

  function tick(timestamp) {
    if (!startTime) startTime = timestamp

    const elapsed = timestamp - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easedProgress = easing(progress)

    callback(easedProgress, progress)

    if (progress < 1 && isRunning) {
      animationFrame = requestAnimationFrame(tick)
    } else {
      isRunning = false
    }
  }

  function start() {
    if (isRunning) return

    isRunning = true
    startTime = null
    animationFrame = requestAnimationFrame(tick)
  }

  function stop() {
    isRunning = false
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
      animationFrame = null
    }
  }

  function pause() {
    isRunning = false
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
      animationFrame = null
    }
  }

  function resume() {
    if (isRunning) return
    isRunning = true
    animationFrame = requestAnimationFrame(tick)
  }

  return {
    start,
    stop,
    pause,
    resume,
    get isRunning() {
      return isRunning
    }
  }
}

/**
 * 创建动画补间
 * @param {Object} from - 起始值
 * @param {Object} to - 目标值
 * @param {number} duration - 持续时间
 * @param {Function} easing - 缓动函数
 * @param {Function} update - 更新回调
 * @returns {Promise} - 动画完成的Promise
 */
export function createTween(from, to, duration, easing, update) {
  return new Promise((resolve) => {
    const startTime = performance.now()

    function tick(currentTime) {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easedProgress = easing(progress)

      // 计算当前值
      const current = {}
      for (const key in from) {
        if (typeof from[key] === 'number' && typeof to[key] === 'number') {
          current[key] = from[key] + (to[key] - from[key]) * easedProgress
        } else {
          current[key] = progress < 1 ? from[key] : to[key]
        }
      }

      update(current, easedProgress)

      if (progress < 1) {
        requestAnimationFrame(tick)
      } else {
        resolve()
      }
    }

    requestAnimationFrame(tick)
  })
}

/**
 * 创建动画循环
 * @param {Function} callback - 回调函数
 * @param {number} fps - 帧率
 * @returns {Object} - 循环控制对象
 */
export function createAnimationLoop(callback, fps = 60) {
  let animationFrame = null
  let lastTime = 0
  const interval = 1000 / fps
  let isRunning = false

  function tick(currentTime) {
    if (!isRunning) return

    if (currentTime - lastTime >= interval) {
      callback(currentTime - lastTime)
      lastTime = currentTime
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

/**
 * 批量应用动画
 * @param {Array} elements - 元素数组
 * @param {Object} animation - 动画配置
 * @param {Object} options - 选项
 */
export function batchAnimate(elements, animation, options = {}) {
  const {
    stagger = 0,
    delay = 0,
    onComplete
  } = options

  let completed = 0
  const total = elements.length

  elements.forEach((element, index) => {
    setTimeout(() => {
      if (element && element.animate) {
        const anim = element.animate(animation.keyframes, {
          duration: animation.duration || 300,
          easing: animation.easing || 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
          fill: 'forwards',
          ...animation.options
        })

        anim.onfinish = () => {
          completed++
          if (completed === total && onComplete) {
            onComplete()
          }
        }
      } else {
        completed++
        if (completed === total && onComplete) {
          onComplete()
        }
      }
    }, delay + index * stagger)
  })
}

/**
 * 创建动画队列
 * @returns {Object} - 队列控制对象
 */
export function createAnimationQueue() {
  const queue = []
  let isProcessing = false

  function add(animation) {
    queue.push(animation)
    if (!isProcessing) {
      processNext()
    }
  }

  async function processNext() {
    if (queue.length === 0) {
      isProcessing = false
      return
    }

    isProcessing = true
    const animation = queue.shift()

    try {
      if (typeof animation === 'function') {
        await animation()
      } else if (animation instanceof Promise) {
        await animation
      }
    } catch (error) {
      console.error('Animation error:', error)
    }

    processNext()
  }

  function clear() {
    queue.length = 0
    isProcessing = false
  }

  return {
    add,
    clear,
    get isProcessing() {
      return isProcessing
    },
    get queueLength() {
      return queue.length
    }
  }
}

/**
 * 检查动画支持
 * @returns {Object} - 支持信息
 */
export function checkAnimationSupport() {
  const support = {
    webAnimations: typeof Element.prototype.animate === 'function',
    cssAnimations: typeof document.createElement('div').style.animationName !== 'undefined',
    cssTransitions: typeof document.createElement('div').style.transition !== 'undefined',
    requestAnimationFrame: typeof requestAnimationFrame === 'function',
    performance: typeof performance !== 'undefined' && typeof performance.now === 'function'
  }

  return support
}

/**
 * 优化动画性能
 * @param {HTMLElement} element - 目标元素
 * @param {Object} styles - 样式
 */
export function optimizeAnimation(element, styles = {}) {
  // 启用硬件加速
  if (styles.transform) {
    element.style.transform = styles.transform
    element.style.willChange = 'transform'
  }

  // 使用 opacity 动画
  if (styles.opacity !== undefined) {
    element.style.opacity = styles.opacity
    element.style.willChange = element.style.willChange
      ? element.style.willChange + ', opacity'
      : 'opacity'
  }

  // 避免布局抖动
  if (styles.left || styles.top) {
    element.style.position = 'absolute'
  }
}

/**
 * 创建动画回调
 * @param {Object} callbacks - 回调函数对象
 * @returns {Object} - 动画回调配置
 */
export function createAnimationCallbacks(callbacks = {}) {
  const {
    onStart,
    onUpdate,
    onComplete,
    onCancel,
    onError
  } = callbacks

  return {
    onstart: onStart,
    onupdate: onUpdate,
    onfinish: onComplete,
    oncancel: onCancel,
    onerror: onError
  }
}

// 导出所有工具函数
export default {
  createAnimationSequence,
  createStaggerAnimation,
  createSpringAnimation,
  createEasingFunction,
  createAnimationTimer,
  createTween,
  createAnimationLoop,
  batchAnimate,
  createAnimationQueue,
  checkAnimationSupport,
  optimizeAnimation,
  createAnimationCallbacks
}
