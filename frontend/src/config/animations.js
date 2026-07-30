/**
 * 动画配置文件
 * 统一管理所有动画参数，便于维护和调整
 */

// 缓动函数
export const easings = {
  // iOS 风格缓动
  ios: {
    default: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    spring: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    smooth: 'cubic-bezier(0.4, 0, 0.2, 1)'
  },
  // 猛兽派对风格缓动
  party: {
    soft: 'cubic-bezier(0.25, 0.1, 0.25, 1)',
    bouncy: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    elastic: 'cubic-bezier(0.64, 0.57, 0.67, 1.53)'
  },
  // 通用缓动
  linear: 'linear',
  ease: 'ease',
  easeIn: 'ease-in',
  easeOut: 'ease-out',
  easeInOut: 'ease-in-out'
}

// 动画时长
export const durations = {
  // 瞬间（用于状态切换）
  instant: 0,
  // 快速（用于微交互）
  fast: 150,
  // 正常（用于一般动画）
  normal: 300,
  // 慢速（用于复杂动画）
  slow: 500,
  // 更慢（用于页面过渡）
  slower: 800
}

// 动画延迟
export const delays = {
  none: 0,
  small: 50,
  medium: 100,
  large: 200
}

// 交错动画配置
export const stagger = {
  // 列表项交错
  list: {
    delay: 50,
    max: 10
  },
  // 网格交错
  grid: {
    delay: 30,
    max: 20
  },
  // 渐进式
  progressive: {
    delay: 100,
    max: 5
  }
}

// 预定义动画
export const presets = {
  // 进入动画
  enter: {
    fadeIn: {
      from: { opacity: 0 },
      to: { opacity: 1 },
      duration: durations.normal,
      easing: easings.ios.default
    },
    slideUp: {
      from: { opacity: 0, transform: 'translateY(20px)' },
      to: { opacity: 1, transform: 'translateY(0)' },
      duration: durations.normal,
      easing: easings.ios.default
    },
    slideDown: {
      from: { opacity: 0, transform: 'translateY(-20px)' },
      to: { opacity: 1, transform: 'translateY(0)' },
      duration: durations.normal,
      easing: easings.ios.default
    },
    slideLeft: {
      from: { opacity: 0, transform: 'translateX(20px)' },
      to: { opacity: 1, transform: 'translateX(0)' },
      duration: durations.normal,
      easing: easings.ios.default
    },
    slideRight: {
      from: { opacity: 0, transform: 'translateX(-20px)' },
      to: { opacity: 1, transform: 'translateX(0)' },
      duration: durations.normal,
      easing: easings.ios.default
    },
    scale: {
      from: { opacity: 0, transform: 'scale(0.9)' },
      to: { opacity: 1, transform: 'scale(1)' },
      duration: durations.normal,
      easing: easings.ios.default
    },
    bounce: {
      from: { opacity: 0, transform: 'scale(0.3)' },
      to: { opacity: 1, transform: 'scale(1)' },
      duration: durations.slow,
      easing: easings.ios.bounce
    },
    zoom: {
      from: { opacity: 0, transform: 'scale(0.5)' },
      to: { opacity: 1, transform: 'scale(1)' },
      duration: durations.normal,
      easing: easings.ios.spring
    }
  },
  // 退出动画
  exit: {
    fadeOut: {
      from: { opacity: 1 },
      to: { opacity: 0 },
      duration: durations.fast,
      easing: easings.easeIn
    },
    slideDown: {
      from: { opacity: 1, transform: 'translateY(0)' },
      to: { opacity: 0, transform: 'translateY(20px)' },
      duration: durations.fast,
      easing: easings.easeIn
    },
    slideUp: {
      from: { opacity: 1, transform: 'translateY(0)' },
      to: { opacity: 0, transform: 'translateY(-20px)' },
      duration: durations.fast,
      easing: easings.easeIn
    },
    scale: {
      from: { opacity: 1, transform: 'scale(1)' },
      to: { opacity: 0, transform: 'scale(0.9)' },
      duration: durations.fast,
      easing: easings.easeIn
    }
  },
  // 交互反馈动画
  interaction: {
    press: {
      transform: 'scale(0.95)',
      duration: durations.fast,
      easing: easings.ios.default
    },
    hover: {
      transform: 'scale(1.02)',
      duration: durations.fast,
      easing: easings.ios.default
    },
    tap: {
      transform: 'scale(0.98)',
      duration: 100,
      easing: easings.ios.default
    }
  },
  // 特效动画
  effects: {
    jelly: {
      keyframes: [
        { transform: 'scale(1, 1)', offset: 0 },
        { transform: 'scale(0.95, 1.05)', offset: 0.25 },
        { transform: 'scale(1.05, 0.95)', offset: 0.5 },
        { transform: 'scale(0.98, 1.02)', offset: 0.75 },
        { transform: 'scale(1, 1)', offset: 1 }
      ],
      duration: durations.slow,
      easing: easings.party.bouncy
    },
    wobble: {
      keyframes: [
        { transform: 'rotate(0deg)', offset: 0 },
        { transform: 'rotate(5deg)', offset: 0.15 },
        { transform: 'rotate(-5deg)', offset: 0.3 },
        { transform: 'rotate(3deg)', offset: 0.45 },
        { transform: 'rotate(-3deg)', offset: 0.6 },
        { transform: 'rotate(1deg)', offset: 0.75 },
        { transform: 'rotate(0deg)', offset: 1 }
      ],
      duration: durations.slow,
      easing: easings.party.soft
    },
    shake: {
      keyframes: [
        { transform: 'translateX(0)', offset: 0 },
        { transform: 'translateX(-10px)', offset: 0.15 },
        { transform: 'translateX(10px)', offset: 0.3 },
        { transform: 'translateX(-5px)', offset: 0.45 },
        { transform: 'translateX(5px)', offset: 0.6 },
        { transform: 'translateX(-2px)', offset: 0.75 },
        { transform: 'translateX(2px)', offset: 0.9 },
        { transform: 'translateX(0)', offset: 1 }
      ],
      duration: durations.slow,
      easing: easings.party.soft
    },
    pulse: {
      keyframes: [
        { transform: 'scale(1)', opacity: 1, offset: 0 },
        { transform: 'scale(1.05)', opacity: 0.8, offset: 0.5 },
        { transform: 'scale(1)', opacity: 1, offset: 1 }
      ],
      duration: 1000,
      easing: easings.easeInOut,
      iterations: Infinity
    },
    float: {
      keyframes: [
        { transform: 'translateY(0px)', offset: 0 },
        { transform: 'translateY(-10px)', offset: 0.5 },
        { transform: 'translateY(0px)', offset: 1 }
      ],
      duration: 3000,
      easing: easings.easeInOut,
      iterations: Infinity
    },
    glow: {
      keyframes: [
        { boxShadow: '0 0 5px rgba(255, 158, 181, 0.5)', offset: 0 },
        { boxShadow: '0 0 20px rgba(255, 158, 181, 0.8)', offset: 0.5 },
        { boxShadow: '0 0 5px rgba(255, 158, 181, 0.5)', offset: 1 }
      ],
      duration: 2000,
      easing: easings.easeInOut,
      iterations: Infinity
    },
    shimmer: {
      keyframes: [
        { backgroundPosition: '-200% 0', offset: 0 },
        { backgroundPosition: '200% 0', offset: 1 }
      ],
      duration: 1500,
      easing: easings.linear,
      iterations: Infinity
    }
  }
}

// Vue Transition 配置
export const transitions = {
  // 淡入淡出
  fade: {
    enter: {
      opacity: 0
    },
    enterActive: {
      transition: `opacity ${durations.normal}ms ${easings.ios.default}`
    },
    leave: {
      opacity: 1
    },
    leaveActive: {
      transition: `opacity ${durations.fast}ms ${easings.easeIn}`
    }
  },
  // 滑入滑出
  slide: {
    enter: {
      opacity: 0,
      transform: 'translateY(20px)'
    },
    enterActive: {
      transition: `all ${durations.normal}ms ${easings.ios.default}`
    },
    leave: {
      opacity: 1,
      transform: 'translateY(0)'
    },
    leaveActive: {
      transition: `all ${durations.fast}ms ${easings.easeIn}`
    }
  },
  // 缩放
  scale: {
    enter: {
      opacity: 0,
      transform: 'scale(0.9)'
    },
    enterActive: {
      transition: `all ${durations.normal}ms ${easings.ios.default}`
    },
    leave: {
      opacity: 1,
      transform: 'scale(1)'
    },
    leaveActive: {
      transition: `all ${durations.fast}ms ${easings.easeIn}`
    }
  },
  // 弹性
  bounce: {
    enter: {
      opacity: 0,
      transform: 'scale(0.3)'
    },
    enterActive: {
      transition: `all ${durations.slow}ms ${easings.ios.bounce}`
    },
    leave: {
      opacity: 1,
      transform: 'scale(1)'
    },
    leaveActive: {
      transition: `all ${durations.fast}ms ${easings.easeIn}`
    }
  }
}

// 动画性能优化配置
export const performance = {
  // 启用硬件加速
  enableHardwareAcceleration: true,
  // 使用 transform 代替 top/left
  useTransform: true,
  // 使用 opacity 代替 visibility
  useOpacity: true,
  // 避免布局抖动
  avoidLayoutThrashing: true,
  // 使用 will-change
  useWillChange: true
}

// 响应式动画配置
export const responsive = {
  // 移动端禁用复杂动画
  mobile: {
    disableComplexAnimations: true,
    reduceMotion: true,
    simplifiedEffects: true
  },
  // 桌面端完整动画
  desktop: {
    disableComplexAnimations: false,
    reduceMotion: false,
    simplifiedEffects: false
  }
}

// 导出默认配置
export default {
  easings,
  durations,
  delays,
  stagger,
  presets,
  transitions,
  performance,
  responsive
}
