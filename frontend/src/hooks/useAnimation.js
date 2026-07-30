/**
 * 动画钩子函数
 * 提供常用的动画效果和交互反馈
 */

import { ref, onMounted, onUnmounted } from 'vue'

/**
 * 元素进入动画钩子
 * @param {string} animation - 动画类型
 * @param {number} delay - 延迟时间
 */
export function useEnterAnimation(animation = 'fade-in', delay = 0) {
  const elementRef = ref(null)
  const isVisible = ref(false)

  onMounted(() => {
    setTimeout(() => {
      isVisible.value = true
    }, delay)
  })

  return {
    elementRef,
    isVisible,
    animationClass: `animate-${animation}`
  }
}

/**
 * 交错动画钩子
 * @param {number} stagger - 交错延迟
 * @param {number} count - 元素数量
 */
export function useStaggerAnimation(stagger = 50, count = 10) {
  const delays = ref([])

  onMounted(() => {
    delays.value = Array.from({ length: count }, (_, i) => i * stagger)
  })

  function getDelay(index) {
    return delays.value[index] || 0
  }

  return {
    delays,
    getDelay
  }
}

/**
 * 滚动触发动画钩子
 * @param {object} options - 配置选项
 */
export function useScrollAnimation(options = {}) {
  const {
    threshold = 0.1,
    rootMargin = '0px 0px -50px 0px',
    once = true
  } = options

  const elementRef = ref(null)
  const isVisible = ref(false)
  let observer = null

  onMounted(() => {
    if (!elementRef.value) return

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            isVisible.value = true
            if (once) {
              observer.unobserve(entry.target)
            }
          } else if (!once) {
            isVisible.value = false
          }
        })
      },
      { threshold, rootMargin }
    )

    observer.observe(elementRef.value)
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
    }
  })

  return {
    elementRef,
    isVisible
  }
}

/**
 * 鼠标跟随动画钩子
 */
export function useMouseAnimation() {
  const mouseX = ref(0)
  const mouseY = ref(0)
  const isMoving = ref(false)

  let moveTimer = null

  function onMouseMove(event) {
    mouseX.value = event.clientX
    mouseY.value = event.clientY
    isMoving.value = true

    clearTimeout(moveTimer)
    moveTimer = setTimeout(() => {
      isMoving.value = false
    }, 100)
  }

  onMounted(() => {
    window.addEventListener('mousemove', onMouseMove)
  })

  onUnmounted(() => {
    window.removeEventListener('mousemove', onMouseMove)
    clearTimeout(moveTimer)
  })

  return {
    mouseX,
    mouseY,
    isMoving
  }
}

/**
 * 弹性动画钩子
 * @param {object} options - 配置选项
 */
export function useSpringAnimation(options = {}) {
  const {
    stiffness = 100,
    damping = 10,
    mass = 1
  } = options

  const position = ref({ x: 0, y: 0 })
  const velocity = ref({ x: 0, y: 0 })
  const target = ref({ x: 0, y: 0 })
  const isAnimating = ref(false)

  let animationFrame = null

  function update() {
    const dx = target.value.x - position.value.x
    const dy = target.value.y - position.value.y

    const ax = (stiffness * dx - damping * velocity.value.x) / mass
    const ay = (stiffness * dy - damping * velocity.value.y) / mass

    velocity.value.x += ax * 0.016 // 60fps
    velocity.value.y += ay * 0.016

    position.value.x += velocity.value.x * 0.016
    position.value.y += velocity.value.y * 0.016

    // 检查是否停止
    const isSettled =
      Math.abs(dx) < 0.01 &&
      Math.abs(dy) < 0.01 &&
      Math.abs(velocity.value.x) < 0.01 &&
      Math.abs(velocity.value.y) < 0.01

    if (!isSettled) {
      animationFrame = requestAnimationFrame(update)
    } else {
      isAnimating.value = false
      position.value = { ...target.value }
    }
  }

  function setTarget(x, y) {
    target.value = { x, y }
    if (!isAnimating.value) {
      isAnimating.value = true
      update()
    }
  }

  function stop() {
    if (animationFrame) {
      cancelAnimationFrame(animationFrame)
      animationFrame = null
    }
    isAnimating.value = false
  }

  onUnmounted(() => {
    stop()
  })

  return {
    position,
    velocity,
    target,
    isAnimating,
    setTarget,
    stop
  }
}

/**
 * 拖拽动画钩子
 * @param {object} options - 配置选项
 */
export function useDragAnimation(options = {}) {
  const {
    boundary = 'parent',
    smooth = true
  } = options

  const position = ref({ x: 0, y: 0 })
  const isDragging = ref(false)
  const dragOffset = ref({ x: 0, y: 0 })

  let element = null

  function startDrag(event, el) {
    element = el
    isDragging.value = true

    const clientX = event.touches ? event.touches[0].clientX : event.clientX
    const clientY = event.touches ? event.touches[0].clientY : event.clientY

    dragOffset.value = {
      x: clientX - position.value.x,
      y: clientY - position.value.y
    }

    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', stopDrag)
    document.addEventListener('touchmove', onDrag, { passive: false })
    document.addEventListener('touchend', stopDrag)

    event.preventDefault()
  }

  function onDrag(event) {
    if (!isDragging.value) return

    const clientX = event.touches ? event.touches[0].clientX : event.clientX
    const clientY = event.touches ? event.touches[0].clientY : event.clientY

    let newX = clientX - dragOffset.value.x
    let newY = clientY - dragOffset.value.y

    // 边界限制
    if (boundary === 'parent' && element) {
      const parent = element.parentElement
      if (parent) {
        const rect = parent.getBoundingClientRect()
        const elRect = element.getBoundingClientRect()

        newX = Math.max(0, Math.min(newX, rect.width - elRect.width))
        newY = Math.max(0, Math.min(newY, rect.height - elRect.height))
      }
    } else if (boundary === 'viewport') {
      const elRect = element.getBoundingClientRect()
      newX = Math.max(0, Math.min(newX, window.innerWidth - elRect.width))
      newY = Math.max(0, Math.min(newY, window.innerHeight - elRect.height))
    }

    position.value = { x: newX, y: newY }

    if (event.cancelable) {
      event.preventDefault()
    }
  }

  function stopDrag() {
    isDragging.value = false
    element = null

    document.removeEventListener('mousemove', onDrag)
    document.removeEventListener('mouseup', stopDrag)
    document.removeEventListener('touchmove', onDrag)
    document.removeEventListener('touchend', stopDrag)
  }

  onUnmounted(() => {
    stopDrag()
  })

  return {
    position,
    isDragging,
    startDrag
  }
}

/**
 * 动画序列钩子
 * @param {Array} sequence - 动画序列
 */
export function useAnimationSequence(sequence = []) {
  const currentIndex = ref(-1)
  const isPlaying = ref(false)
  const progress = ref(0)

  let timeout = null

  async function play() {
    if (isPlaying.value) return

    isPlaying.value = true
    currentIndex.value = 0

    for (let i = 0; i < sequence.length; i++) {
      currentIndex.value = i
      progress.value = (i / sequence.length) * 100

      const step = sequence[i]

      if (step.animation) {
        await step.animation()
      }

      if (step.duration) {
        await new Promise(resolve => {
          timeout = setTimeout(resolve, step.duration)
        })
      }
    }

    currentIndex.value = sequence.length
    progress.value = 100
    isPlaying.value = false
  }

  function stop() {
    clearTimeout(timeout)
    isPlaying.value = false
    currentIndex.value = -1
    progress.value = 0
  }

  function reset() {
    stop()
  }

  onUnmounted(() => {
    stop()
  })

  return {
    currentIndex,
    isPlaying,
    progress,
    play,
    stop,
    reset
  }
}

/**
 * 视差动画钩子
 * @param {number} speed - 视差速度
 */
export function useParallax(speed = 0.5) {
  const offset = ref(0)
  const elementRef = ref(null)

  function onScroll() {
    if (!elementRef.value) return

    const rect = elementRef.value.getBoundingClientRect()
    const windowHeight = window.innerHeight

    if (rect.top < windowHeight && rect.bottom > 0) {
      const scrollProgress = (windowHeight - rect.top) / (windowHeight + rect.height)
      offset.value = (scrollProgress - 0.5) * speed * 100
    }
  }

  onMounted(() => {
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', onScroll)
  })

  return {
    elementRef,
    offset,
    style: {
      transform: `translateY(${offset.value}px)`
    }
  }
}

/**
 * 打字机动画钩子
 * @param {string} text - 文本内容
 * @param {number} speed - 打字速度
 */
export function useTypewriter(text, speed = 50) {
  const displayText = ref('')
  const isTyping = ref(false)
  const isComplete = ref(false)

  let timeout = null
  let index = 0

  function start() {
    if (isTyping.value) return

    isTyping.value = true
    isComplete.value = false
    displayText.value = ''
    index = 0

    typeNext()
  }

  function typeNext() {
    if (index < text.length) {
      displayText.value += text[index]
      index++
      timeout = setTimeout(typeNext, speed)
    } else {
      isTyping.value = false
      isComplete.value = true
    }
  }

  function stop() {
    clearTimeout(timeout)
    isTyping.value = false
  }

  function reset() {
    stop()
    displayText.value = ''
    index = 0
    isComplete.value = false
  }

  onUnmounted(() => {
    stop()
  })

  return {
    displayText,
    isTyping,
    isComplete,
    start,
    stop,
    reset
  }
}

// 导出所有钩子
export default {
  useEnterAnimation,
  useStaggerAnimation,
  useScrollAnimation,
  useMouseAnimation,
  useSpringAnimation,
  useDragAnimation,
  useAnimationSequence,
  useParallax,
  useTypewriter
}
