# 🎨 动画系统使用指南

> **文档版本**：v1.0  
> **更新日期**：2026-07-30  
> **适用范围**：喵喵语音 🐾 前端动画系统

---

## 📋 概述

本文档介绍喵喵语音项目的动画系统，包括动画组件、钩子函数、CSS工具类等的使用方法。

动画系统遵循以下设计原则：
- **iOS 风格**：平滑、优雅、有弹性
- **猛兽派对风格**：柔软、可爱、有亲和力
- **性能优先**：使用 GPU 加载、避免布局抖动
- **无障碍支持**：支持减少动画偏好

---

## 🧩 动画组件

### 1. AnimatedButton - 带动画的按钮

**文件位置**：`frontend/src/components/common/AnimatedButton.vue`

**使用方法**：
```vue
<template>
  <AnimatedButton
    variant="primary"
    size="medium"
    :loading="isLoading"
    @click="handleClick"
  >
    点击我
  </AnimatedButton>
</template>

<script setup>
import AnimatedButton from '@/components/common/AnimatedButton.vue'
import { ref } from 'vue'

const isLoading = ref(false)

function handleClick() {
  isLoading.value = true
  // 执行操作...
}
</script>
```

**属性说明**：
| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| variant | String | 'primary' | 按钮样式：primary, secondary, ghost, danger |
| size | String | 'medium' | 按钮尺寸：small, medium, large |
| disabled | Boolean | false | 是否禁用 |
| loading | Boolean | false | 是否显示加载状态 |

**特性**：
- ✅ 点击弹性缩放效果
- ✅ 波纹点击反馈
- ✅ 加载状态动画
- ✅ 多种样式变体

---

### 2. AnimatedList - 列表动画

**文件位置**：`frontend/src/components/common/AnimatedList.vue`

**使用方法**：
```vue
<template>
  <AnimatedList animation="slide-up" :stagger="50">
    <div v-for="item in items" :key="item.id" :data-index="item.index">
      {{ item.name }}
    </div>
  </AnimatedList>
</template>

<script setup>
import AnimatedList from '@/components/common/AnimatedList.vue'
import { ref } from 'vue'

const items = ref([
  { id: 1, name: '项目 1', index: 0 },
  { id: 2, name: '项目 2', index: 1 },
  { id: 3, name: '项目 3', index: 2 }
])
</script>
```

**属性说明**：
| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| tag | String | 'div' | 容器标签 |
| animation | String | 'slide-up' | 动画类型：slide-up, slide-right, fade, scale |
| stagger | Number | 50 | 交错延迟（毫秒） |
| containerClass | String/Object/Array | '' | 容器类名 |

**特性**：
- ✅ 列表项依次进入
- ✅ 支持多种动画类型
- ✅ 可配置交错延迟

---

### 3. TransitionWrapper - 过渡动画包装器

**文件位置**：`frontend/src/components/common/TransitionWrapper.vue`

**使用方法**：
```vue
<template>
  <TransitionWrapper name="bounce" mode="out-in">
    <div v-if="show" key="content">
      内容
    </div>
  </TransitionWrapper>
</template>

<script setup>
import TransitionWrapper from '@/components/common/TransitionWrapper.vue'
import { ref } from 'vue'

const show = ref(true)
</script>
```

**属性说明**：
| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| name | String | 'fade' | 动画类型：fade, slide-up, slide-down, slide-left, slide-right, scale, bounce, flip, zoom |
| mode | String | 'out-in' | 过渡模式：out-in, in-out, default |
| duration | Number/Object | 300 | 动画时长（毫秒） |

**特性**：
- ✅ 多种预定义动画
- ✅ 支持进入/离开事件
- ✅ 可配置过渡模式

---

### 4. AnimatedToast - 通知动画

**文件位置**：`frontend/src/components/common/AnimatedToast.vue`

**使用方法**：
```vue
<template>
  <AnimatedToast ref="toastRef" />
</template>

<script setup>
import AnimatedToast from '@/components/common/AnimatedToast.vue'
import { ref } from 'vue'

const toastRef = ref(null)

// 显示通知
function showSuccess() {
  toastRef.value.success('操作成功！')
}

function showError() {
  toastRef.value.error('操作失败，请重试')
}

function showWarning() {
  toastRef.value.warning('请注意')
}

function showInfo() {
  toastRef.value.info('提示信息')
}
</script>
```

**方法说明**：
| 方法 | 参数 | 说明 |
|------|------|------|
| show(message, type, duration) | message: String, type: String, duration: Number | 显示通知 |
| success(message, duration) | message: String, duration: Number | 显示成功通知 |
| error(message, duration) | message: String, duration: Number | 显示错误通知 |
| warning(message, duration) | message: String, duration: Number | 显示警告通知 |
| info(message, duration) | message: String, duration: Number | 显示信息通知 |
| removeToast(id) | id: Number | 移除指定通知 |

**特性**：
- ✅ 多种通知类型
- ✅ 自动消失
- ✅ 堆叠显示
- ✅ 进度条动画
- ✅ 点击关闭

---

### 5. LoadingAnimation - 加载动画

**文件位置**：`frontend/src/components/common/LoadingAnimation.vue`

**使用方法**：
```vue
<template>
  <!-- 骨架屏 -->
  <LoadingAnimation type="skeleton" text="加载中..." />

  <!-- 脉冲加载 -->
  <LoadingAnimation type="pulse" size="large" />

  <!-- 旋转加载 -->
  <LoadingAnimation type="spinner" />

  <!-- 波浪加载 -->
  <LoadingAnimation type="wave" />

  <!-- 弹跳加载 -->
  <LoadingAnimation type="bounce" />

  <!-- 喵喵加载（品牌特色） -->
  <LoadingAnimation type="meow" text="加载中..." />

  <!-- 覆盖层加载 -->
  <LoadingAnimation type="spinner" :overlay="true" text="处理中..." />
</template>

<script setup>
import LoadingAnimation from '@/components/common/LoadingAnimation.vue'
</script>
```

**属性说明**：
| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| type | String | 'spinner' | 动画类型：skeleton, pulse, spinner, wave, bounce, meow, default |
| size | String | 'medium' | 尺寸：small, medium, large |
| text | String | '' | 加载文字 |
| overlay | Boolean | false | 是否显示覆盖层 |

**特性**：
- ✅ 多种动画类型
- ✅ 可配置尺寸
- ✅ 支持覆盖层
- ✅ 品牌特色动画（喵喵）

---

## 🎣 动画钩子函数

### 1. useEnterAnimation - 进入动画

**文件位置**：`frontend/src/hooks/useAnimation.js`

**使用方法**：
```vue
<template>
  <div ref="elementRef" :class="{ 'animate-visible': isVisible }">
    内容
  </div>
</template>

<script setup>
import { useEnterAnimation } from '@/hooks/useAnimation'

const { elementRef, isVisible } = useEnterAnimation('fade-in', 200)
</script>
```

**参数说明**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| animation | String | 'fade-in' | 动画类型 |
| delay | Number | 0 | 延迟时间（毫秒） |

**返回值**：
| 属性 | 类型 | 说明 |
|------|------|------|
| elementRef | Ref | 元素引用 |
| isVisible | Ref<Boolean> | 是否可见 |
| animationClass | String | 动画类名 |

---

### 2. useScrollAnimation - 滚动触发动画

**文件位置**：`frontend/src/hooks/useAnimation.js`

**使用方法**：
```vue
<template>
  <div ref="elementRef" :class="{ 'animate-visible': isVisible }">
    内容
  </div>
</template>

<script setup>
import { useScrollAnimation } from '@/hooks/useAnimation'

const { elementRef, isVisible } = useScrollAnimation({
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px',
  once: true
})
</script>
```

**参数说明**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| threshold | Number | 0.1 | 可见度阈值 |
| rootMargin | String | '0px 0px -50px 0px' | 根元素边距 |
| once | Boolean | true | 是否只触发一次 |

**返回值**：
| 属性 | 类型 | 说明 |
|------|------|------|
| elementRef | Ref | 元素引用 |
| isVisible | Ref<Boolean> | 是否可见 |

---

### 3. useDragAnimation - 拖拽动画

**文件位置**：`frontend/src/hooks/useAnimation.js`

**使用方法**：
```vue
<template>
  <div
    :style="{ transform: `translate(${position.x}px, ${position.y}px)` }"
    @mousedown="startDrag($event, $el)"
  >
    可拖拽元素
  </div>
</template>

<script setup>
import { useDragAnimation } from '@/hooks/useAnimation'

const { position, isDragging, startDrag } = useDragAnimation({
  boundary: 'viewport',
  smooth: true
})
</script>
```

**参数说明**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| boundary | String | 'parent' | 边界限制：parent, viewport, none |
| smooth | Boolean | true | 是否平滑 |

**返回值**：
| 属性 | 类型 | 说明 |
|------|------|------|
| position | Ref<{x, y}> | 当前位置 |
| isDragging | Ref<Boolean> | 是否正在拖拽 |
| startDrag | Function | 开始拖拽函数 |

---

### 4. useTypewriter - 打字机动画

**文件位置**：`frontend/src/hooks/useAnimation.js`

**使用方法**：
```vue
<template>
  <span>{{ displayText }}</span>
  <button @click="start">开始</button>
  <button @click="reset">重置</button>
</template>

<script setup>
import { useTypewriter } from '@/hooks/useAnimation'

const { displayText, isTyping, isComplete, start, stop, reset } = useTypewriter(
  '欢迎使用喵喵语音！',
  50
)
</script>
```

**参数说明**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| text | String | - | 文本内容 |
| speed | Number | 50 | 打字速度（毫秒/字符） |

**返回值**：
| 属性 | 类型 | 说明 |
|------|------|------|
| displayText | Ref<String> | 当前显示的文本 |
| isTyping | Ref<Boolean> | 是否正在打字 |
| isComplete | Ref<Boolean> | 是否完成 |
| start | Function | 开始函数 |
| stop | Function | 停止函数 |
| reset | Function | 重置函数 |

---

## 🎨 CSS 工具类

### 动画类

**文件位置**：`frontend/src/styles/animation-utils.css`

#### 进入动画
```css
.fade-in          /* 淡入 */
.fade-in-up       /* 上淡入 */
.fade-in-down     /* 下淡入 */
.fade-in-left     /* 左淡入 */
.fade-in-right    /* 右淡入 */
.slide-in-up      /* 上滑入 */
.slide-in-down    /* 下滑入 */
.slide-in-left    /* 左滑入 */
.slide-in-right   /* 右滑入 */
.scale-in         /* 缩放进入 */
.bounce-in        /* 弹入 */
.flip-in          /* 翻转进入 */
.rotate-in        /* 旋转进入 */
```

#### 退出动画
```css
.fade-out          /* 淡出 */
.fade-out-up       /* 上淡出 */
.fade-out-down     /* 下淡出 */
.fade-out-left     /* 左淡出 */
.fade-out-right    /* 右淡出 */
.slide-out-up      /* 上滑出 */
.slide-out-down    /* 下滑出 */
.slide-out-left    /* 左滑出 */
.slide-out-right   /* 右滑出 */
.scale-out         /* 缩放退出 */
.bounce-out        /* 弹出 */
```

#### 强调动画
```css
.pulse            /* 脉冲 */
.flash            /* 闪烁 */
.bounce           /* 弹跳 */
.shake            /* 摇晃 */
.wobble           /* 抖动 */
.swing            /* 摆动 */
.spin             /* 旋转 */
```

#### 特效动画
```css
.float            /* 悬浮 */
.glow             /* 发光 */
.shimmer          /* 闪烁 */
.typewriter       /* 打字机 */
```

#### 交互动画
```css
.tap-effect       /* 点击效果 */
.hover-effect     /* 悬浮效果 */
.focus-effect     /* 聚焦效果 */
```

#### 状态动画
```css
.loading          /* 加载中 */
.success          /* 成功状态 */
.error            /* 错误状态 */
```

#### 交错延迟
```css
.stagger-1        /* 延迟 50ms */
.stagger-2        /* 延迟 100ms */
.stagger-3        /* 延迟 150ms */
.stagger-4        /* 延迟 200ms */
.stagger-5        /* 延迟 250ms */
.stagger-6        /* 延迟 300ms */
.stagger-7        /* 延迟 350ms */
.stagger-8        /* 延迟 400ms */
.stagger-9        /* 延迟 450ms */
.stagger-10       /* 延迟 500ms */
```

#### 持续时间
```css
.duration-fast    /* 0.15s */
.duration-normal  /* 0.3s */
.duration-slow    /* 0.5s */
.duration-slower  /* 0.8s */
.duration-slowest /* 1s */
```

#### 缓动函数
```css
.easing-linear    /* 线性 */
.easing-ease      /* 缓动 */
.easing-ease-in   /* 缓入 */
.easing-ease-out  /* 缓出 */
.easing-ease-in-out /* 缓入缓出 */
.easing-ios       /* iOS 风格 */
.easing-spring    /* 弹性 */
.easing-bounce    /* 弹跳 */
```

#### 性能优化
```css
.gpu-accelerated  /* 硬件加速 */
.will-animate     /* 预优化 */
.smooth-scroll    /* 平滑滚动 */
```

---

## ⚙️ 动画配置

### 配置文件

**文件位置**：`frontend/src/config/animations.js`

**主要配置项**：

```javascript
// 缓动函数
easings.ios.default        // iOS 默认缓动
easings.ios.spring         // iOS 弹性缓动
easings.ios.bounce         // iOS 弹跳缓动
easings.party.soft         // 猛兽派对柔和缓动
easings.party.bouncy       // 猛兽派对弹性缓动

// 动画时长
durations.instant          // 0ms
durations.fast             // 150ms
durations.normal           // 300ms
durations.slow             // 500ms
durations.slower           // 800ms

// 预定义动画
presets.enter.fadeIn       // 淡入动画
presets.enter.slideUp      // 上滑动画
presets.enter.bounce       // 弹入动画
presets.exit.fadeOut       // 淡出动画
presets.interaction.press  // 按压效果
presets.effects.jelly      // 果冻效果
presets.effects.float      // 悬浮效果
```

---

## 🎯 最佳实践

### 1. 性能优化

```css
/* 使用 GPU 加速属性 */
.optimized {
  transform: translateZ(0);
  backface-visibility: hidden;
  will-change: transform, opacity;
}

/* 避免布局抖动 */
.position-absolute {
  position: absolute;
  left: 0;
  top: 0;
}

/* 使用 transform 代替 top/left */
.use-transform {
  transform: translateX(100px);
  /* 代替 left: 100px; */
}
```

### 2. 响应式动画

```css
/* 移动端简化动画 */
@media (max-width: 768px) {
  .mobile-simplify {
    animation-duration: 0.2s;
    transition-duration: 0.2s;
  }
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 3. 动画组合

```vue
<template>
  <TransitionWrapper name="slide-up" mode="out-in">
    <AnimatedList v-if="show" animation="fade-in" :stagger="100">
      <div v-for="item in items" :key="item.id">
        {{ item.name }}
      </div>
    </AnimatedList>
  </TransitionWrapper>
</template>
```

### 4. 交互反馈

```vue
<template>
  <AnimatedButton
    variant="primary"
    @click="handleClick"
  >
    点击
  </AnimatedButton>

  <div class="hover-effect">
    悬浮效果
  </div>

  <div class="tap-effect" @click="handleTap">
    点击效果
  </div>
</template>
```

---

## 🐛 常见问题

### Q1: 动画不生效？

**检查项**：
1. 确保元素有正确的初始状态
2. 检查动画类名是否正确
3. 确认动画时长和延迟设置
4. 检查是否有 CSS 覆盖

### Q2: 动画卡顿？

**解决方案**：
1. 使用 GPU 加速属性（transform, opacity）
2. 避免动画中改变布局属性（width, height, top, left）
3. 使用 `will-change` 提示浏览器
4. 减少同时动画的元素数量

### Q3: 如何禁用动画？

**方法**：
1. 使用 `prefers-reduced-motion` 媒体查询
2. 添加 `duration-0` 类
3. 使用 JavaScript 检测用户偏好

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
```

---

## 📚 相关资源

- [MDN Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [Vue Transition](https://vuejs.org/guide/built-ins/transition.html)
- [iOS Human Interface Guidelines - Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [Material Design - Motion](https://material.io/design/motion/)

---

> **注意**：本文档会随动画系统更新而更新，请关注版本变更。
