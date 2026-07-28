import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './styles/main.css'

const app = createApp(App)

// 使用状态管理
app.use(createPinia())

// 使用路由
app.use(router)

// 挂载应用
app.mount('#app')
