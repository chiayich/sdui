import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import logger from './lib/logger'

// 配置日志服务
logger.setAppName('sdui-frontend')
// API基础URL与应用相同
logger.setApiUrl('')

// 记录首次加载时间
logger.info('Application starting', {
  timestamp: new Date().toISOString(),
  url: window.location.href,
  userAgent: navigator.userAgent
})

// 路由变化时记录导航
router.beforeEach((to, from) => {
  logger.logNavigation(to.fullPath, { from: from.fullPath })
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  logger.error('Vue Error', {
    error: String(err),
    info,
    component: vm?.$options?.name || 'Unknown'
  })
}

app.mount('#app') 