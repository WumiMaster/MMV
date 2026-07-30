/**
 * 动画指令系统
 * 提供v-animate指令，支持多种动画效果
 */

// 预定义动画
const animations = {
  // 进入动画
  'fade-in': {
    from: { opacity: 0 },
    to: { opacity: 1 }
  },
  'slide-up': {
    from: { opacity: 0, transform: 'translateY(20px)' },
    to: { opacity: 1, transform: 'translateY(0)' }
  },
  'slide-down': {
    from: { opacity: 0, transform: 'translateY(-20px)' },
    to: { opacity: 1, transform: 'translateY(0)' }
  },
  'slide-left': {
    from: { opacity: 0, transform: 'translateX(20px)' },
    to: { opacity: 1, transform: 'translateX(0)' }
  },
  'slide-right': {
    from: { opacity: 0, transform: 'translateX(-20px)' },
    to: { opacity: 1, transform: 'translateX(0)' }
  },
  'scale': {
    from: { opacity: 0, transform: 'scale(0.8)' },
    to: { opacity: 1, transform: 'scale(1)' }
  },
  'bounce': {
    from: { opacity: 0, transform: 'scale(0.3)' },
    to: { opacity: 1, transform: 'scale(1)' },
    easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
  },
  'flip': {
    from: { opacity: 0, transform: 'perspective(400px) rotateY(90deg)' },
    to: { opacity: 1, transform: 'perspective(400px) rotateY(0)' }
  },
  'zoom': {
    from: { opacity: 0, transform: 'scale(0.5)' },
    to: { opacity: 1, transform: 'scale(1)' }
  },
  'rotate': {
    from: { opacity: 0, transform: 'rotate(-180deg) scale(0.5)' },
    to: { opacity: 1, transform: 'rotate(0) scale(1)' }
  }
}

// 交错动画延迟计算
function getStaggerDelay(el, stagger) {
  const parent = el.parentElement
  if (!parent) return 0

  const siblings = Array.from(parent.children)
  const index = siblings.indexOf(el)
  return index * stagger
}

// 应用动画
function applyAnimation(el, binding) {
  const {
    value = 'fade-in',
    modifiers = {}
  } = binding

  // 解析动画配置
  let animationName = value
  let duration = 300
  let delay = 0
  let easing = 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
  let stagger = 0

  // 处理修饰符
  if (modifiers.slow) duration = 600
  if (modifiers.fast) duration = 150
  if (modifiers.delay) delay = 300

  // 处理对象形式的配置
  if (typeof value === 'object') {
    animationName = value.name || 'fade-in'
    duration = value.duration || duration
    delay = value.delay || delay
    easing = value.easing || easing
    stagger = value.stagger || 0
  }

  // 获取动画配置
  const animation = animations[animationName]
  if (!animation) {
    console.warn(`未知的动画类型: ${animationName}`)
    return
  }

  // 计算交错延迟
  if (stagger > 0) {
    delay = getStaggerDelay(el, stagger)
  }

  // 设置初始状态
  Object.assign(el.style, {
    ...animation.from,
    transition: `all ${duration}ms ${easing} ${delay}ms`,
    willChange: 'transform, opacity'
  })

  // 触发动画
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      Object.assign(el.style, animation.to)
    })
  })

  // 动画完成后清理
  setTimeout(() => {
    el.style.transition = ''
    el.style.willChange = ''
  }, duration + delay + 100)
}

// 观察器配置
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
}

// 交叉观察器
let observer = null

function createObserver() {
  if (observer) return observer

  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target
        const binding = el.__animateBinding__

        if (binding) {
          applyAnimation(el, binding)
          observer.unobserve(el)
        }
      }
    })
  }, observerOptions)

  return observer
}

// 指令定义
export const vAnimate = {
  mounted(el, binding) {
    // 保存绑定信息
    el.__animateBinding__ = binding

    // 处理修饰符
    const { modifiers } = binding

    if (modifiers.hover) {
      // Hover动画
      el.addEventListener('mouseenter', () => {
        const animation = animations[binding.value] || animations['scale']
        Object.assign(el.style, {
          transition: 'transform 0.2s ease',
          transform: animation.to.transform || 'scale(1.05)'
        })
      })

      el.addEventListener('mouseleave', () => {
        el.style.transform = ''
      })
      return
    }

    if (modifiers.click) {
      // 点击动画
      el.addEventListener('click', () => {
        el.style.animation = 'none'
        el.offsetHeight // 触发重绘
        el.style.animation = `${binding.value || 'bounce'} 0.5s ease`
      })
      return
    }

    if (modifiers.visible) {
      // 可见时动画
      const obs = createObserver()
      obs.observe(el)
      return
    }

    // 默认：立即动画
    applyAnimation(el, binding)
  },

  updated(el, binding) {
    if (binding.value !== binding.oldValue) {
      el.__animateBinding__ = binding
      applyAnimation(el, binding)
    }
  },

  unmounted(el) {
    if (observer) {
      observer.unobserve(el)
    }
    delete el.__animateBinding__
  }
}

// 动画工具函数
export function animate(element, keyframes, options = {}) {
  const {
    duration = 300,
    easing = 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    delay = 0,
    fill = 'forwards'
  } = options

  return element.animate(keyframes, {
    duration,
    easing,
    delay,
    fill
  })
}

// 弹性动画
export function bounce(element, options = {}) {
  return animate(element, [
    { transform: 'scale(1)', offset: 0 },
    { transform: 'scale(1.1)', offset: 0.3 },
    { transform: 'scale(0.95)', offset: 0.6 },
    { transform: 'scale(1.02)', offset: 0.8 },
    { transform: 'scale(1)', offset: 1 }
  ], {
    duration: options.duration || 500,
    easing: 'ease-out',
    ...options
  })
}

// 摇晃动画
export function shake(element, options = {}) {
  return animate(element, [
    { transform: 'translateX(0)', offset: 0 },
    { transform: 'translateX(-10px)', offset: 0.15 },
    { transform: 'translateX(10px)', offset: 0.3 },
    { transform: 'translateX(-5px)', offset: 0.45 },
    { transform: 'translateX(5px)', offset: 0.6 },
    { transform: 'translateX(-2px)', offset: 0.75 },
    { transform: 'translateX(2px)', offset: 0.9 },
    { transform: 'translateX(0)', offset: 1 }
  ], {
    duration: options.duration || 600,
    easing: 'ease-out',
    ...options
  })
}

// 脉冲动画
export function pulse(element, options = {}) {
  return animate(element, [
    { transform: 'scale(1)', opacity: 1, offset: 0 },
    { transform: 'scale(1.05)', opacity: 0.8, offset: 0.5 },
    { transform: 'scale(1)', opacity: 1, offset: 1 }
  ], {
    duration: options.duration || 1000,
    iterations: options.iterations || Infinity,
    easing: 'ease-in-out',
    ...options
  })
}

// 闪烁动画
export function flash(element, options = {}) {
  return animate(element, [
    { opacity: 1, offset: 0 },
    { opacity: 0, offset: 0.25 },
    { opacity: 1, offset: 0.5 },
    { opacity: 0, offset: 0.75 },
    { opacity: 1, offset: 1 }
  ], {
    duration: options.duration || 1000,
    iterations: options.iterations || 3,
    easing: 'linear',
    ...options
  })
}

// 导出所有动画函数
export const animations_library = {
  animate,
  bounce,
  shake,
  pulse,
  flash
}

export default vAnimate
